## Handler机制分析

### 目录

* ##### [框架图](#1)

* ##### [主线程Handler和Looper](#2)

<h3 id="1">框架图</h3>

<img src="../assets/images/edraw/handler.png?v=1">

和上图有关的Message的几个成员变量：

```java
public final class Message implements Parcelable {
    /*package*/ Handler target;

    /*package*/ Runnable callback;

    // sometimes we store linked lists of these things
    /*package*/ Message next;
}
```

<h3 id="2">主线程Handler和Looper</h3>

```java
public final class ActivityThread extends ClientTransactionHandler {
    final Looper mLooper = Looper.myLooper();
    final H mH = new H();
    static volatile Handler sMainThreadHandler;  // set once in main()
    public static void main(String[] args) {
    	Looper.prepareMainLooper();
    	ActivityThread thread = new ActivityThread();
    	if (sMainThreadHandler == null) {
            sMainThreadHandler = thread.getHandler();
        }
        Looper.loop();
    }
    final Handler getHandler() {
        return mH;
    }
    class H extends Handler {
    	// ...
    }
}
```