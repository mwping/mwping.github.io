## 待办事项

#### 开源框架心得

1. 大而全的谨慎使用；
2. 放弃更新的不用；
3. 加入中间层，方便后续替换；

#### Glide vs Picasso

|图片加载库|Glide|Picasso|
|:-:|:-:|:-:|
|自动确定图片大小|支持，使用ViewTreeObserver.<br>addOnPreDrawListener监听View尺寸|不支持，需要调用<br>resize(width, height)|
|缓存策略|4种|2种(全图/无缓存)|
|感知生命周期|支持，onDestroy会清掉弱引用的内存|不支持|
|gif|支持|不支持|

**Glide缓存策略**

|图片加载库|优点|缺点|
|:-:|:-:|:-:|
|原图|不需要每次请求网络|占磁盘，每次需要缩放|
|缩略图|占用磁盘空间少，不需要额外缩放|每种尺寸都需要请求网络|
|原图+缩略图|不需要每次请求网络，<br>不需要额外缩放|占磁盘|
|不缓存|每次请求最新|最慢|

#### OkHttp

从request出发，依次经历

1. 自定义拦截
2. 重试拦截器
3. Bridge拦截器
4. Cache拦截器
5. Connect拦截器
6. 自定义网络拦截器
7. CallServer拦截器

**重试拦截器**

|状态码|含义|相关返回头|目的|
|:-:|:-:|:-:|:-:|
|303|See Other|Location|重定向|
|408|Request Timeout|Retry-After|重试|
|503|Service Unavailable|Retry-After|重试|

**Bridge拦截器**

|Header字段|作用|
|:-:|:-:|
|Accept-Encoding|gzip|
|Content-Type|数据格式，如text/plain; charset=utf-8|
|Content-Length|请求body长度|
|Connection|Keep-Alive|
|Cookie|cookie|
|User-Agent|客户端标志|

**Cache拦截器**

|请求头|返回头|
|:-:|:-:|
|If-None-Match|ETag|
|If-Modified-Since|Last-Modified|
|过期判断|Cache-Control|

**Connect拦截器**

连接池复用，复用条件：

1. 连接池空闲，即此连接的上一次客户端-服务器请求应答完毕；
2. 请求地址的主机名host相等；

**CallServer拦截器**

负责写request、读response。

#### Retrofit

**使用Builder模式创建Retrofit实例**
```java
    retrofit = new Retrofit.Builder()
            .baseUrl(url)
            .addConverterFactory(GsonConverterFactory.create())
            .client(client).build();
```

**使用动态代理生成HttpServiceMethod**

```java
  public <T> T create(final Class<T> service) {
    Utils.validateServiceInterface(service);
    if (validateEagerly) {
      eagerlyValidateMethods(service);
    }
    return (T) Proxy.newProxyInstance(service.getClassLoader(), new Class<?>[] { service },
        new InvocationHandler() {
          private final Platform platform = Platform.get();
          private final Object[] emptyArgs = new Object[0];

          @Override public Object invoke(Object proxy, Method method, @Nullable Object[] args)
              throws Throwable {
            // If the method is a method from Object then defer to normal invocation.
            if (method.getDeclaringClass() == Object.class) {
              return method.invoke(this, args);
            }
            if (platform.isDefaultMethod(method)) {
              return platform.invokeDefaultMethod(method, service, proxy, args);
            }
            return loadServiceMethod(method).invoke(args != null ? args : emptyArgs);
          }
        });
  }
```

**使用工厂模式创建Converter**

```
public final class GsonConverterFactory extends Converter.Factory {

}
```

**使用MainThreadExecutor将回调交给主线程**
```java
    static class MainThreadExecutor implements Executor {
      private final Handler handler = new Handler(Looper.getMainLooper());

      @Override public void execute(Runnable r) {
        handler.post(r);
      }
    }
```




