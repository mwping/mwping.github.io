## Glide解析


监听View的尺寸：

```java
    ViewTreeObserver observer = view.getViewTreeObserver();
    layoutListener = new SizeDeterminerLayoutListener(this);
    observer.addOnPreDrawListener(layoutListener);
```

获取到尺寸之后，SingleRequest在onSizeReady时开始加载：
```java
	engine.load()
```

取第一层缓存：HashMap

Engine.java
```java
loadFromActiveResources(){
	// ...
}
```
ActiveResources.java:
```java
  final Map<Key, ResourceWeakReference> activeEngineResources = new HashMap<>();
```

取第二层缓存：LruCache
```java
public class LruCache<T, Y> {
  private final Map<T, Y> cache = new LinkedHashMap<>(100, 0.75f, true);
}
```

启动异步任务，Engine的jobs属性包含所有运行中的异步任务：
```java
final class Jobs {
	private final Map<Key, EngineJob<?>> jobs = new HashMap<>();
}
```

每个EngineJob都包含一个Callback列表，多个请求加载同一个图片(地址相同+目标宽高相同)，不需要另起异步任务，只需要在现有任务添加回调监听即可：
```java
    EngineJob<?> current = jobs.get(key, onlyRetrieveFromCache);
    if (current != null) {
      current.addCallback(cb, callbackExecutor);
    }
```

全局的Glide对象有两个线程池：

1.网络请求线程池：通过Runtime.getRuntime().availableProcessors()计算出最合适的线程数，但是不超过4个线程，构建出来的ThreadPoolExecutor属性是：

* maximumPoolSize=corePoolSize=4;
* keepAliveTime=0;
* workQueue=PriorityBlockingQueue;

2.磁盘缓存线程池：

* maximumPoolSize=corePoolSize=1;
* keepAliveTime=0;
* workQueue=PriorityBlockingQueue;

DecodeJob实现了Runnable，Comparable接口，任务越新，优先级越高。
```java
  @Override
  public int compareTo(@NonNull DecodeJob<?> other) {
    int result = getPriority() - other.getPriority();
    if (result == 0) {
      result = order - other.order;
    }
    return result;
  }
```

开始读取磁盘缓存。磁盘的缓存策略是：

* ALL: 缓存原图文件+缩略图两个文件；
* DATA：只缓存原图；
* RESOURCE：只缓存缩略图；
* NONE：不使用磁盘缓存；




