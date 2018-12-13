## App启动流程

App启动涉及到两个非常关键的系统服务：

1. PackageManagerService(以下简称PMS)，管理应用程序的静态信息，主要是安装包的信息；
2. ActivityManagerService(以下简称AMS)，管理应用程序的运行时信息，例如Activity启动涉及的一系列数据结构。

### 检查Activity是否注册

**为了启动Activity，用户(比如Launcher)把要启动的Activity的包名、类全限定名放在Intent(意图)中，传给AMS。**

![](../assets/images/intent.png?v=1)

**AMS收到请求后，去PMS查找此Activity是否有在Manifest中注册。**

apk安装完成或系统启动，PMS会扫描system/app、/data/app/目录下面的apk文件：

![](../assets/images/data_app.png?v=1)

![](../assets/images/system_app.png?v=1)

然后使用PackageParser类解析每个apk的Manifest文件，把每个Activity的信息封装成PackageParser.Activity类，然后统一放到```ArrayMap<ComponentName, PackageParser.Activity>```数据结构(在PMS类里面的字段名叫mActivities)进行管理：

PackageManagerService.java
```java
        // Keys are String (activity class name), values are Activity.
        private final ArrayMap<ComponentName, PackageParser.Activity> mActivities
            = new ArrayMap<ComponentName, PackageParser.Activity>();
```

查找Activity是否注册的过程，在PMS内部就是```mActivities.get(Activity类名)!=null```的过程。

如果未注册，则失败抛出```ActivityNotFoundException```异常；如果已注册，则进行下一步：启动App进程。

### 启动进程

AMS从PMS获取到的结果是待启动的Activity已注册，且检查发现这个Activity之前没有启动过对应的进程，于是给zygote发送消息，申请fork一个子进程，并指定这个进程的主类是```ActivityThread```。zygote fork出子进程之后，执行```ActivityThread```的main方法，main方法中创建了一个ActivityThread实例：
```java
    ActivityThread thread = new ActivityThread();
```

新进程此时并不知道需要启动Activity，而是回去询问AMS自己下一步如何操作：

```java
    private void attach(boolean system) {
        try {
             mgr.attachApplication(mAppThread);
        } catch (RemoteException ex) {
            throw ex.rethrowFromSystemServer();
        }
    }
```
AMS的attachApplication方法被调用，做了关键的两件事：

1. 调用用户进程的bindApplication方法，并传递了大量参数；
2. 启动Activity；

ActivityManagerService.java:
```java
    private final boolean attachApplicationLocked(IApplicationThread thread,
            int pid) {
        thread.bindApplication(...);
        //...
        if (mStackSupervisor.attachApplicationLocked()) {
            didSomething = true;
        }
    }
```

ActivityStackSupervisor.java:
```java
    boolean attachApplicationLocked(ProcessRecord app){
        realStartActivityLocked(app);
    }
    final boolean realStartActivityLocked(app){
        app.thread.scheduleLaunchActivity(intent);
    }
```

这里的thread在App进程是```ApplicationThread```实例，是ActivityThread的成员变量：

ActivityThread.java
```java
    final ApplicationThread mAppThread = new ApplicationThread();
```

ApplicationThread按先后顺序对应执行了两个操作：
```java
    public final void bindApplication(){
        //...
    }
    public final void scheduleLaunchActivity(){
        //...
    }
```

bindApplication()在App进程中，由子线程经过Handler交给了主线程来处理:

```java
    public final void bindApplication(String processName, ...) {
        AppBindData data = new AppBindData();
        data.processName = processName;
        sendMessage(H.BIND_APPLICATION, data);
    }

    private void handleBindApplication(AppBindData data) {
        //...
    }
```

`handleBindApplication`处理AMS传递过来的如下信息：

**1.修改进程名为：processName**

App进程刚启动之时，进程名称叫`<pre-initialized>`：

ActivityThread.java:
```java
    public static void main(String[] args) {
        Process.setArgV0("<pre-initialized>");
    }
```
handleBindApplication方法进行修改：
```java
    private void handleBindApplication(AppBindData data) {
        Process.setArgV0(data.processName);
    }
```

通常情况下，正式的进程名是app定义的包名。通过`adb shell ps`命令、Android Studio工具可以查看进程列表：

![](../assets/images/proc_init.png?v=1)
![](../assets/images/proc_servicemanager.png?v=1)
![](../assets/images/proc_zygote.png?v=1)
![](../assets/images/proc_system_server.png?v=1)
![](../assets/images/proc_calender.png?v=1)
![](../assets/images/as_process_name.png?v=1)

日历应用的进程id=2902，name就等于\"com.android.calendar\"。这里可以顺便了解一下进程树：

1. init进程是servicemanager和zygote的父进程
2. zygote是system_server和App的父进程。

![](../assets/images/proc_tree.png?v=1)

**2.如果targetSdkVersion版本<=12，修改AsyncTask类的默认线程池**

```java
    // If the app is Honeycomb MR1 or earlier, switch its AsyncTask
    // implementation to use the pool executor.  Normally, we use the
    // serialized executor as the default. This has to happen in the
    // main thread so the main looper is set right.
    if (data.appInfo.targetSdkVersion <= android.os.Build.VERSION_CODES.HONEYCOMB_MR1) {
        AsyncTask.setDefaultExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
    }
```

对于每个App进程，AsyncTask默认共用同一个线程池。对于Android3.1及以下的版本，由上面的方法把默认线程池改为THREAD_POOL_EXECUTOR：
```java
    /**
     * An {@link Executor} that can be used to execute tasks in parallel.
     */
    public static final Executor THREAD_POOL_EXECUTOR;

    static {
        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
                CORE_POOL_SIZE, MAXIMUM_POOL_SIZE, KEEP_ALIVE_SECONDS, TimeUnit.SECONDS,
                sPoolWorkQueue, sThreadFactory);
        threadPoolExecutor.allowCoreThreadTimeOut(true);
        THREAD_POOL_EXECUTOR = threadPoolExecutor;
    }
```

而对于Android3.1以上(不包括)，会把多线程转化为单线程执行：

```java
    /**
     * An {@link Executor} that executes tasks one at a time in serial
     * order.  This serialization is global to a particular process.
     */
    public static final Executor SERIAL_EXECUTOR = new SerialExecutor();

    private static class SerialExecutor implements Executor {
        final ArrayDeque<Runnable> mTasks = new ArrayDeque<Runnable>();
        Runnable mActive;

        public synchronized void execute(final Runnable r) {
            mTasks.offer(new Runnable() {
                public void run() {
                    try {
                        r.run();
                    } finally {
                        scheduleNext();
                    }
                }
            });
            if (mActive == null) {
                scheduleNext();
            }
        }

        protected synchronized void scheduleNext() {
            if ((mActive = mTasks.poll()) != null) {
                THREAD_POOL_EXECUTOR.execute(mActive);
            }
        }
    }
```
所以能发现，调用AsyncTask.execute方法，多个任务是按顺序依次执行的。

**3.创建一系列实例**

* 创建LoadedApk实例；

```java
    new LoadedApk(ActivityThread, ApplicationInfo, ...);
```

* 创建Instrumentation实例；

```java
    mInstrumentation = new Instrumentation();
```

* 创建ContextImpl实例；

```java
    new ContextImpl(ActivityThread, LoadedApk...);
```

* 创建Application实例并调用其attach方法绑定前面的ContextImpl，Application的attach会调用自己的attachBaseContext方法。最后调用Application的onCreate方法。这里能知道Application生命周期，attachBaseContext先于onCreate。

```java
    //className=Manifest文件指定的自定义Application类全限定名或者android.app.Application
    Class<?> clazz = PathClassLoader.loadClass(className);
    Application app = (Application)clazz.newInstance();
    app.attach(context);
    app.onCreate();
```

到这里总结一下：

在Application的onCreate这个时机，Application实例拥有了以下数据：

1. mBase：ContextImpl；
2. mLoadedApk：LoadedApk；

mBase(ContextImpl实例)拥有的数据：

1. mBasePackageName：应用包名，如com.github.mwping.app；
2. mMainThread：本进程ActivityThread实例；
3. mPackageInfo：LoadedApk，和Application的mLoadedApk指向同一个；

mLoadedApk(LoadedApk实例)拥有的数据：

1. mActivityThread：和mBase的mMainThread是同一个；
2. mAppDir：App安装路径下的apk文件路径，如/data/app/com.github.mwping.app-wkpuxbdLJjsHdxJ7-rruDg==/base.apk
3. mApplication: 指向Application实例；
4. mApplicationInfo：AMS传递过来的ApplicationInfo；
5. mClassLoader：PathClassLoader。

LoadedApk的mApplicationInfo拥有的数据：

1. processName：进程名(等于包名);
2. scanSourceDir/scanPublicSourceDir：App安装路径下的apk文件路径，和上面的mAppDir是同一个；
3. taskAffinity：默认的taskAffinity，等于包名，如com.github.mwping.app。

Application创建完成，接着就是Activity的启动。

### 启动Activity

Activity的启动由AMS调用App进程的scheduleLaunchActivity发起。

**创建ActivityClientRecord实例，接收AMS传递过来的参数，发送消息，交给主线程handleLaunchActivity方法处理：**
```java
    public final void scheduleLaunchActivity(Intent intent, ActivityInfo info){
        ActivityClientRecord r = new ActivityClientRecord();
        r.intent = intent;
        r.activityInfo = info;
        sendMessage(H.LAUNCH_ACTIVITY, r);
    }
```

**创建属于Activity的ContextImpl**

```java
    ContextImpl appContext = ContextImpl.createActivityContext(
                this, r.packageInfo, r.activityInfo, r.token, displayId, r.overrideConfig);
```

**反射创建Activity实例，用到的ClassLoader和创建Application的是同一个**

```java
    //className为类的全限定名，如com.github.mwping.app.MainActivity
    Activity activity = (Activity)cl.loadClass(className).newInstance();
```

**调用Activity的attach方法**

1. 指定mBase为刚刚创建的ContextImpl；
2. 创建PhoneWindow，指定给Activity自己的mWindow；
3. 指定mUiThread = Thread.currentThread();
4. 调用onCreate()，在onCreate方法通过setContentView把内容布局(R.layout.activity_main)加载到整个View树中；
5. 调用onStart();
6. 启动记录保存在ActivityThread的ArrayMap<IBinder, ActivityClientRecord> mActivities中。

**handleResumeActivity**

1. 把Activity的View树根节点DecorView添加到WindowManagerImpl；
2. DecorView调用measure；
3. DecorView调用layout；
4. DecorView调用draw;

在这里Activity界面变成可见了。

### AMS管理Activity栈、任务、Activity启动记录等信息

使用命令行分析Stack、Task、Activity三者的关系：

```
    adb shell dumpsys activity activities
```

**AMS使用ActivityStackSupervisor集中管理所有Stack**

```java
    // TODO: Add listener for removal of references.
    /** Mapping from (ActivityStack/TaskStack).mStackId to their current state */
    SparseArray<ActivityStack> mStacks = new SparseArray<>();
```

每个ActivityStack管理自己的TaskRecord：
```java
    /**
     * The back history of all previous (and possibly still
     * running) activities.  It contains #TaskRecord objects.
     */
    private final ArrayList<TaskRecord> mTaskHistory = new ArrayList<>();
```

每个TaskRecord又管理自己的Activity

```java
    /** List of all activities in the task arranged in history order */
    final ArrayList<ActivityRecord> mActivities;
```



