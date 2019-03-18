
## 团队工作

<img src="../../assets/images/teamwork.png?v=1" width="660">


**纵向架构**


1.底层

第三方库，封装的复用模块；

2.中间层：

* 适配器类：(埋点库、认证库切换)；
* SDK代理类：懒加载，防止SDK方法本身的耗时、类加载耗时；
* 装饰器：包装Glide的Cache，记录超大图片；

3.上层：MVP、MVVM

**横向**

平级业务模块的路由通信；

**性能优化**

开发阶段：
1. LeakCanary
2. BlockCanary
3. MemoryProfile
4. CPU Profile
5. systrace
6. 代理类，sdk懒加载；

线上监控：

1. 启动耗时；
2. 帧率采样+开关(3天后关闭)；
3. 大图监控；

**疑难问题**

埋点+curl导出用户时间线。

**WebView**