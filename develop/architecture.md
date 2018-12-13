## 架构模式

### 参考文档

[https://github.com/googlesamples/android-architecture](https://github.com/googlesamples/android-architecture)

### 为什么要用架构模式？

设想一个场景：
你接手一个旧项目，可能有以下几个特点：
1. 各种大类；
2. 各种大方法；
3. 很多包，各种命名方案；
4. 很多类，也是各种命名方案，眼花缭乱；
5. 耦合性太强，牵一发而动全身。

要解决这一类问题，就需要找到一种策略将项目解耦，各个部分分别进行抽象，封装，类和方法根据这个策略进行合理的组织，这个策略就是架构模式。

### MVC模式
* Model：模型
* View：视图
* Controller：控制器

MVC模式简单理解：
1. 视图响应用户点击；
2. 点击事件交由控制器根据业务逻辑请求修改Model；
3. Model更新之后，触发视图更新(例如通过观察者模式)。
整体是一个V->C->M->V的环形通信。

MVC的优点：
*  一定程度的分层，解耦；

缺点：
*  视图需要访问模型数据

### MVP模式
* Model：模型
* View：视图
* Presenter：和Controller类似

MVP模式的简单理解：
1. View层几乎不包含任何逻辑，它响应用户操作，并将这些操作交给Presenter处理，Presenter处理完成之后会把结果(例如对Model的查询结果)交给View层以刷新视图；
2. Presenter承载业务逻辑，处理View上交的用户事件，修改/查询Model，通过回调接收结果，并将结果转发给View层以刷新视图；
3. Model承载数据管理功能，可以是内存、数据库或最简单的SharedPreference。

MVP和MVC的最主要的区别在于各个层之间的通信方向，把V->C->M->V改造成了V<->P<->M，模型与视图完全分离，即View对Model一无所知。

MVP的一般要素：
* BasePresenter：所有Presenter的公共接口；
* BaseView：所有View的公共接口，提供setPresenter方法；
* Activity：作为View层或者负责创建Fragment和Presenter；
* Fragment：作为View层，实现BaseView接口；
* Presenter：实现BasePresenter接口，构造函数传递View层(即Fragment)和Model对象；

![MVP](https://github.com/googlesamples/android-architecture/wiki/images/mvp.png)

MVP优点：
* MV完全分离；
* 分层开发，没有View层也可以模拟数据测试Presenter。

MVP缺点：
* Presenter和View交互会过于频繁，联系过于紧密，随着业务的复杂化，很可能会变成一对一的绑定关系。

### MVVM模式

和MVP类似：
* Model：模型，角色和在MVP一致；
* ViewModel，角色和Presenter类似，负责去Model请求数据，不同点在于更新View的方式：MVP里Presenter可以直接调用View对象的方法，而ViewModel不持有View的引用，即MVP的VP是双向交互，MVVM是V->VM的单向通信。
* View：和在MVP中的角色类似。

MVVM的一般要素：
* Activity：创建ViewModel和Fragment，并把ViewModel赋值给Fragment，也就是View层；
* Fragment：View层，把加载请求发给ViewModel；
* ViewModel：负责从Model加载数据；
* DataBinding：持有ViewModel和View的引用，负责监听ViewModel的数据加载结果并更新View。

![MVVM](https://github.com/googlesamples/android-architecture/wiki/images/mvvm-databinding.png)

为了理解MVVM，举一个极简的例子：
1. Fragment有一个TextView，这个TextView被DataBinding引用；
2. ViewModel有一个回调接口List，属性变化之后会通知这些接口；
3. DataBinding内部拥有一个监听接口，加入到ViewModel回调接口List中；
4. 当ViewModel加载到数据之后，通知DataBinding数据有更新，DataBinding便更新TextView的数据。

MVP和MVVP对比：
* 学习成本：MVP低，MVVM高；
* MVP代码简单，MVVM代码复杂；
* MVP不需要第三方依赖，MVVM需要依赖DataBinding库。

