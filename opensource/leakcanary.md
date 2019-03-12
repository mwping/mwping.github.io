## leakcanary解析

**添加监听**

Application初始化：
```java
LeakCanary.install(this);
```

监听Activity生命周期的回调，ActivityRefWatcher.java:
```java
  public static void install(@NonNull Context context, @NonNull RefWatcher refWatcher) {
    Application application = (Application) context.getApplicationContext();
    ActivityRefWatcher activityRefWatcher = new ActivityRefWatcher(application, refWatcher);

    application.registerActivityLifecycleCallbacks(activityRefWatcher.lifecycleCallbacks);
  }
```
ActivityRefWatcher.java
```java
  private final Application.ActivityLifecycleCallbacks lifecycleCallbacks =
      new ActivityLifecycleCallbacksAdapter() {
        @Override public void onActivityDestroyed(Activity activity) {
          refWatcher.watch(activity);
        }
      };
```

**监控目标**

在onActivityDestroyed方法中，监控Activity(Fragment类似)：

1. 对目标Activity创建弱引用，每个弱引用设置一个特殊的key；
2. 5秒后，检查弱引用的queue，如果包含这个key，说明已经没有强引用了，从retainedKeys移除此key；
3. 否则，触发gc，再次检测，如果仍有强引用，说明Activity可能泄露；
4. 获取dumpFile：Debug.dumpHprofData(fileName)；
5. 调用HeapAnalyzerService分析dump，通知栏展示泄露简介；
6. 点击通知栏打开DisplayLeakActivity展示泄露详情。