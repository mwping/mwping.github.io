## OkHttp详解

### 目录

* ##### [拦截器机制](#1)

* ##### [Http状态码](#2)
  1. [成功：2xx](#2.1)
  2. [重定向：3xx](#2.2)
  3. [Client错误：4xx](#2.3)
  4. [Server错误：5xx](#2.4)

* ##### [重试机制](#3)
  1. [408重试](#3.1)
  2. [503重试](#3.2)
  3. [3xx重试](#3.3)

* ##### [BridgeInterceptor](#4)

* ##### [CacheInterceptor](#5)

* ##### [ConnectInterceptor](#6)

* ##### [CallServerInterceptor](#7)

* ##### [Call.cancel](#8)

* ##### [各种Post请求的处理](#9)
  1. [Post String](#9.1)
  2. [Post Form](#9.2)
  3. [Post File](#9.3)
  4. [Post Multipart](#9.4)

<h3 id="1">拦截器机制</h3>

[wiki:Interceptors](https://github.com/square/okhttp/wiki/Interceptors)一张图说明了OkHttp的拦截器机制：

<img src="https://raw.githubusercontent.com/wiki/square/okhttp/interceptors@2x.png" width="540">

<img src="../../assets/images/okhttp.png?v=1" width="850">

RealCall.java
```java
  Response getResponseWithInterceptorChain() throws IOException {
    // Build a full stack of interceptors.
    List<Interceptor> interceptors = new ArrayList<>();
    interceptors.addAll(client.interceptors());
    interceptors.add(retryAndFollowUpInterceptor);
    interceptors.add(new BridgeInterceptor(client.cookieJar()));
    interceptors.add(new CacheInterceptor(client.internalCache()));
    interceptors.add(new ConnectInterceptor(client));
    if (!forWebSocket) {
      interceptors.addAll(client.networkInterceptors());
    }
    interceptors.add(new CallServerInterceptor(forWebSocket));

    Interceptor.Chain chain = new RealInterceptorChain(interceptors, null, null, null, 0,
        originalRequest, this, eventListener, client.connectTimeoutMillis(),
        client.readTimeoutMillis(), client.writeTimeoutMillis());

    return chain.proceed(originalRequest);
  }
```

拦截器按顺序如下：

1. OkHttpClient.Builder.addInterceptor()方法定义的拦截器;
2. 重试拦截器RetryAndFollowUpInterceptor
3. BridgeInterceptor
4. CacheInterceptor
5. ConnectInterceptor
6. OkHttpClient.Builder.addNetworkInterceptor()方法定义的拦截器;
7. CallServerInterceptor

<h3 id="2">Http状态码</h3>

<h4 id="2.1">成功：2xx</h4> 
<h4 id="2.2">重定向：3xx</h4> 
<h4 id="2.3">Client错误：4xx</h4> 
<h4 id="2.4">Server错误：5xx</h4> 


<h3 id="3">重试机制</h3>

<h4 id="3.1">408重试</h4>

情景：服务器等待客户端请求超时，状态码408(Request Timeout)：
如果服务端返回的Header：\"Retry-After\", \"N\"，N>0，则表示服务器希望客户端在N秒之后再重试，此时客户端放弃；如果没有Retry-After头，或者值为0，则客户端发起重试；如果重试仍然出现408，放弃。

<h4 id="3.2">503重试</h4>

重试机制和408类似，规律是：重试的状态码和初始请求的错误码一致，放弃重试，例如服务器第一次和第二次均返回503，那么客户端不会进行第三次请求。但是如果服务器返回的状态码依次是408，503，408，503依次交替，那么客户端最多会重试20次，之后便抛出异常。

RetryAndFollowUpInterceptor.java
```java
public final class RetryAndFollowUpInterceptor implements Interceptor {
  /**
   * How many redirects and auth challenges should we attempt? Chrome follows 21 redirects; Firefox,
   * curl, and wget follow 20; Safari follows 16; and HTTP/1.0 recommends 5.
   */
  private static final int MAX_FOLLOW_UPS = 20;

  @Override public Response intercept(Chain chain) throws IOException {
      if (++followUpCount > MAX_FOLLOW_UPS) {
        streamAllocation.release(true);
        throw new ProtocolException("Too many follow-up requests: " + followUpCount);
      }
  }
}
```

<h4 id="3.3">3xx重试</h4>

OkHttp的300-303都是同样的重试逻辑：当服务端返回的状态码为其中一个，那么解析Response的Header，找到Location字段。若无此字段，放弃，如果有，读取其值；使用这个值构建请求发起重试。

<h3 id="4">BridgeInterceptor</h3>

gzip相关逻辑在这里处理：

* 为App的请求头加上\"Accept-Encoding\": \"gzip\"；
* 根据服务端的返回头\"Content-Encoding\"，如果其值也等于gzip，则需要进行gzip解压缩再交给App。

post参数也在这里处理，例如构建如下请求
```java
    public static final MediaType JSON
            = MediaType.get("application/json; charset=utf-8");

    RequestBody body = RequestBody.create(JSON, "{\"a\":\"a\"}");
    Request request = new Request.Builder()
            .url(url)
            .post(body)
            .build();
```
BridgeInterceptor会加上如下Header：
```
Content-Type: application/json; charset=utf-8
Content-Length: 9
```

另外，如果用户没有设置Host、Connection、User-Agent这两个请求头，BridgeInterceptor也会补充默认的：
```
Host: localhost:51857
Connection: Keep-Alive
User-Agent: okhttp/3.13.1
```

<h3 id="5">CacheInterceptor</h3>

缓存机制由CacheInterceptor来实现。

* App调用OkHttpClient.Builder().cache(new Cache(getExternalCacheDir(), 1024 * 1024 * 20))来创建缓存目录；
* 初次请求，当response和request的Cache-Control头的值均不为no-store时，网络请求缓存至本地。
* 再次请求，客户端取缓存，如果有ETag，把ETag值取出来，放到请求头\"If-None-Match\"供服务端校验，如果服务器核对此值没有修改，将返回304 Not Modify，客户端可以直接使用已有缓存；
* 如果服务端上次指定了Cache-Control: max-age=N，则客户端计算出当前时间是否处在缓存有效的区间，如果是，则不进行网络请求。
* 如果接口返回了Date或者Last-Modified: Sat, 09 Mar 2019 13:06:48 GMT，下一次请求头加上If-Modified-Since: Sat, 09 Mar 2019 13:06:48 GMT，服务端判断超过了这个时间则返回新数据，否则可以返回304 Not Modify，app继续使用缓存。

<h3 id="6">ConnectInterceptor</h3>

ConnectInterceptor的主要目的是找到可用的socket连接。连接池的复用逻辑在这里处理，用到的是http/1.1 keep-alive=true的属性，tcp连接保活。连接(RealConnection)可复用的依据：

1. 连接池不为空；
2. 连接池空闲，即此连接的上一次客户端-服务器请求应答完毕；
3. 请求地址的主机名host相等；

连接池的保活时间，默认5分钟:
```java
  public ConnectionPool() {
    this(5, 5, TimeUnit.MINUTES);
  }
```
可自定义：
```java
OkHttpClient.Builder().connectionPool(new ConnectionPool(5, 15, TimeUnit.SECONDS));
```

<h3 id="7">CallServerInterceptor</h3>

CallServerInterceptor负责向输出流写入request，并从输入流读取response。

写入request：

1. 写入\"GET / HTTP/1.1"；
2. 写入空行(\"\n\r\")
2. 遍历请求头，按格式\"header.name: header.value\"依次写入，每对Header换行；
3. 换行；
4. 写入requestBody，长度等于请求头\"Content-Length\"的长度。

读response：

1. 读取状态行，如\"HTTP/1.1 200 OK\"；
2. 逐行读取Header，以\":\"为分隔符解析成key: value的形式；如\"Content-Length: 19\"；
3. 从返回头Content-Length字段读取返回body的长度：例如上面的19；
4. 如果返回头\"Connection\: close"，则关闭连接，否则保持连接(keep-alive)；
5. 构造Response对象并返回。
6. 通过Response.body().string()真正的把流读完。

<h3 id="8">Call.cancel</h3>

一个进行中的请求(RealCall)，调用cancel()会关闭socket：
```java
  public static void closeQuietly(Socket socket) {
    if (socket != null) {
      try {
        socket.close();
      } catch (AssertionError e) {
        if (!isAndroidGetsocknameError(e)) throw e;
      } catch (RuntimeException rethrown) {
        throw rethrown;
      } catch (Exception ignored) {
      }
    }
  }
```

<h3 id="9">各种Post请求的处理</h3>

<h4 id="9.1">Post String</h4>
如果格式服务器不支持，则服务器将返回415 Unsupported Media Type。

```java
    public static final MediaType TEXT
            = MediaType.get("text/plain; charset=utf-8");
    RequestBody body = RequestBody.create(TEXT, "hello I am a string");
    Request request = new Request.Builder()
            .url(getUrl())
            .post(body)
            .build();
    Response response = client.newCall(request).execute();
```

请求头：
```
    Content-Type: text/plain; charset=utf-8
    Content-Length: 19
```

请求body为\"hello I am a string\"

<h4 id="9.2">Post Form</h4>

```java
    private void doPostForm() {
        RequestBody formBody = new FormBody.Builder()
                .add("search", "Android")
                .add("from", "mwp")
                .build();
        Request request = new Request.Builder()
                .url("https://zh.wikipedia.org/w/index.php")
                .post(formBody)
                .build();

        try {
            Response response = client.newCall(request).execute();
            Log.d(TAG, "doPostForm: " + response.body().string());
        } catch (IOException e) {
            Log.e(TAG, "doPostForm: ", e);
        }
    }
```

请求头：
```
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 23
```

请求body为\"search=Android&from=mwp\"。


<h4 id="9.3">Post File</h4>

```java
    public static final MediaType MEDIA_TYPE_MARKDOWN
            = MediaType.get("text/x-markdown; charset=utf-8");
    File file = new File(Environment.getExternalStorageDirectory() + "/Download/test.md");
    Request request = new Request.Builder()
            .url("https://api.github.com/markdown/raw")
            .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, file))
            .build();
    Response response = client.newCall(request).execute();
```
请求头
```
    Content-Type: text/x-markdown; charset=utf-8
    Content-Length: 9
```

<h4 id="9.4">Post Multipart</h4>

```java
    File f = new File(Environment.getExternalStorageDirectory() + "/Download/test.md");
            Log.d(TAG, "doPostMultipart: File:" + f.length());
    RequestBody requestBody = new MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("title", "test title")
            .addFormDataPart("content", "file_name",
                    RequestBody.create(TEXT, f))
            .build();

    Request request = new Request.Builder()
            .url(getUrl())
            .post(requestBody)
            .build();
    Response response = client.newCall(request).execute();
```
请求头：
```
    Content-Type: multipart/form-data; boundary=daa37881-9c17-4e83-99c5-08cdd5627d24
    Content-Length: 345
```

