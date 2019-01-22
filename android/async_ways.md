## 异步的几种方式

### 目录

* ##### [继承Thread](#1)

* ##### [使用Runnable](#2)

* ##### [使用Callable和FutureTask](#3)

* ##### [使用Callable、FutureTask和线程池](#4)

<h3 id="1">继承Thread</h3>

```java
    Thread t = new Thread() {
        @Override
        public void run() {
            // ...
        }
    };
    t.start();
```

<h3 id="2">使用Runnable</h3>

```java
    Thread t = new Thread(new Runnable() {
        @Override
        public void run() {
            // ...
        }
    });
    t.start();
```

<h3 id="3">使用Callable和FutureTask</h3>

```java
    Callable<String> callable = new Callable<String>() {
        @Override
        public String call() {
            return "Hello Callable!!!";
        }
    };
    FutureTask<String> futureTask = new FutureTask<>(callable);
    Thread t = new Thread(futureTask);
    t.start();
```

<h3 id="4">使用Callable、FutureTask和线程池</h3>


```java
    Callable<String> callable = new Callable<String>() {
        @Override
        public String call() {
            return "Hello Callable!!!";
        }
    };
    FutureTask<String> futureTask = new FutureTask<>(callable);
    ExecutorService service = Executors.newSingleThreadExecutor();
    service.execute(futureTask);
```
