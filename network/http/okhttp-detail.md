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

* ##### [缓存机制](#5)

* ##### [连接池](#6)

<h3 id="1">拦截器机制</h3>

[wiki:Interceptors](https://github.com/square/okhttp/wiki/Interceptors)一张图说明了OkHttp的拦截器机制：

<img src="https://raw.githubusercontent.com/wiki/square/okhttp/interceptors@2x.png" width="540">

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

<h3 id="5">缓存机制</h3>

缓存机制由CacheInterceptor来实现。

* App调用OkHttpClient.Builder().cache(new Cache(getExternalCacheDir(), 1024 * 1024 * 20))来创建缓存目录；
* 初次请求，当response和request的Cache-Control头的值均不为no-store时，网络请求缓存至本地。
* 再次请求，客户端取缓存，如果有ETag，把ETag值取出来，放到请求头\"If-None-Match\"供服务端校验，如果服务器核对此值没有修改，将返回304 Not Modify，客户端可以直接使用已有缓存；
* 如果服务端上次指定了Cache-Control: max-age=N，则客户端计算出当前时间是否处在缓存有效的区间，如果是，则不进行网络请求。

<h3 id="6">ConnectInterceptor</h3>

* 连接池的逻辑在ConnectInterceptor处理，用到的是http/1.1 keep-alive=true的属性，tcp连接保活。
