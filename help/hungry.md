## 待办事项

#### Handler原理

1. Looper.prepare()方法中，先获取当前线程Thread.currentThread()，记为t；
2. 从t的threadLocals变量，获取到ThreadLocalMap对象；
3. ThreadLocalMap对象内部是一个数组；
4. ThreadLocal<Looper>.set()方法，会把Looper实例放到当前线程的threadLocals的数组中，下标由ThreadLocal确定；
5. Looper的构造方法中，会新建一个MessageQueue实例；
6. Looper.loop()开始进入无限循环，获取不到消息会进入阻塞状态；
7. Handler实例的sendMessage方法，把消息插入到MessageQueue；
8. 获取到消息之后，调用msg.target.dispatchMessage进行分发处理；
9. 如果msg的callback(Runnable类型)不为空，则调用callback的run方法；
10. 否则，调用handler自身的handleMessage方法。

#### App启动过程

1. Intent包名+类名确定目标Class的全限定名，调用AMS启动Activity；
2. AMS查询PMS，校验目标Activity是否在Manifest注册；
3. AMS通过socket向zygote申请fork新进程，指定入口函数ActivityThread.main();
4. 新进程创建完成之后，执行入口main函数，调用Looper.prepareMainLooper()，创建ActivityThread实例；
5. 接着新进程attachApplication通知AMS新进程就绪，然后执行Looper.loop()准备接收AMS的接下来的消息；
6. AMS调用handleBindApplication通知该新进程进行进一步初始化；
7. 通过Class.newInstance()创建Application实例；
8. 调用Application的attachBaseContext()方法；
9. 调用Application的onCreate()方法；
10. AMS接着调用handleLaunchActivity通知App进程需要启动Activity；
11. 同样的，通过Class.newInstance()创建Activity实例；
12. activity的attach方法创建PhoneWindow；
13. activity调用onCreate方法，把setContentView()指定的视图加载进父布局；
14. activity调用onStart();
15. activity调用onResume();
16. 创建ViewRootImpl实例root，
17. 以顶级布局DecorView作为参数，调用root.setView(view, wparams, panelParentView);
18. root.performTraversals();
19. root.performMeasure();
20. root.performLayout();
21. root.performDraw();
22. activity调用onWindowFocusChanged()，真正的界面对用户可见。

#### java的4种引用

|引用类型|回收时机|get()|isEnqueued()|
|:-:|:-:|:-:|:-:|
|强引用|不回收|-|-|
|软引用|OOM之前|强引用被回收之后为null|强引用被回收之后为true|
|弱引用|每次GC|强引用被回收之后为null|强引用被回收之后为true|
|虚引用|不影响|永远为null|强引用被回收之后为true|

#### 垃圾回收的方法

|GC Roots|
|:-:|
|栈帧中的本地变量表引用的对象|
|类静态属性引用的对象|
|类常量引用的对象|
|JNI方法栈引用的对象|

|垃圾收集算法|使用场景|特点|
|:-:|:-:|:-:|
|标记-清除|老年代|内存碎片|
|标记-整理|老年代|额外的整理工作|
|复制|新生代|牺牲10%的Survivor空间|

#### leakcanary原理

1. 初始化时在Application注册监听Activity生命周期；
2. 对onDestroy的Activity进行watch：创建此Activity的弱引用；分配一个特有的key，把key加入监控Set中；
3. 5秒之后，从弱引用的queue中poll元素，如果获取到弱引用，说明强引用已被回收，获取其key，从Set中移除；
4. 否则，调用Runtime.getRuntime().gc()触发GC；
5. 如果仍然存在Activity的强引用，说明Activity可能存在泄漏，调用Debug.dumpHprofData()获取dump信息；
6. 3-5阶段的操作是通过backgroundHandler提交给HandlerThread执行。
7. 在新进程的前台Service中，解析dump数据，找到泄漏Activity的最短引用链，如子线程->Runnable->Activity。

#### 卡顿优化

**因素**

1. CPU竞争：线程数、线程优先级；
2. 界面层级，measure/layout/draw耗时；
3. gc；

**排查**

1. Systrace
2. CPU Profile
3. 过度绘制
4. Layout Inspector
5. GPU条形图

**解决方法**

1. 耗时方法放到子线程；
2. 布局扁平化；
3. 使用线程池；
4. 规划好线程优先级；
5. 内存优化。

**内存抖动**

1. 避免循环体内创建对象；
2. 避免在onDraw创建对象；
3. Bitmap内存缓存；
4. 对象池。

**内存优化点**

* 内部类引用导致Activity的泄漏
* static引用了Activity
* unregisterReceiver
* Cursor对象注意关闭
* 流注意关闭

#### 组件化/模块化

|架构|目的|定位|依赖|
|:-:|:-:|:-:|:-:|
|模块化|隔离|横向|路由跳转|
|组件化|复用|纵向|上下级依赖|


#### http/https

|协议|安全性|端口|成本|
|:-:|:-:|:-:|:-:|
|http|明文|80|低|
|https|加密|443|每个消息加密/解密，SSL握手|

#### tcp/udp

|协议|TCP|UDP|
|:-:|:-:|:-:|
|面向连接|是|否|
|可靠性|是|否|
|顺序控制|是|否|
|重发控制|是|否|
|流量控制|是|否|
|拥塞控制|慢启动|否|
|实时性|低|高|

#### WebView优化点

**图片后加载**

1. onPageStarted: WebSettings.setBlockNetworkImage(true);
2. onPageFinished: WebSettings.setBlockNetworkImage(false);
