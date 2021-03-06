## 设计模式

* ##### [面向对象](#1)
  1. [OO特征](#1.1)
  2. [OO原则](#1.2)
  3. [设计模式一览](#1.3)

* ##### [单例模式(Singleton)](#2)
  1. [意图](#2.1)
  2. [类图](#2.2)
  3. [单例模式VS静态变量](#2.3)

* ##### [策略模式](#3)
  1. [定义](#3.1)
  2. [类图](#3.2)
  3. [应用：TimeInterpolator](#3.3)

* ##### [观察者模式](#4)
  1. [定义](#4.1)
  2. [类图](#4.2)

* ##### [装饰者模式(Decorator)](#5)
  1. [意图](#5.1)
  2. [类图](#5.2)

* ##### [工厂方法模式(Factory Method)](#6)
  1. [意图](#6.1)
  2. [类图](#6.2)
  3. [应用:ThreadFactory](#6.3)

* ##### [抽象工厂模式(Abstract Factory)](#7)
  1. [意图](#7.1)
  2. [类图](#7.2)

* ##### [命令模式](#8)
  1. [定义](#8.1)
  2. [类图](#8.2)
  3. [应用:ThreadPoolExecutor](#8.3)

* ##### [适配器模式(Adapter)](#9)
  1. [意图](#9.1)
  2. [类图](#9.2)

* ##### [外观模式(Facade)](#10)
  1. [意图](#10.1)
  2. [类图](#10.2)

* ##### [模板方法模式](#11)
  1. [定义](#11.1)
  2. [类图](#11.2)
  3. [应用:View.draw](#11.3)

* ##### [迭代器模式](#12)
  1. [定义](#12.1)
  2. [类图](#12.2)

* ##### [组合模式(Composite)](#13)
  1. [意图](#13.1)
  2. [类图](#13.2)

* ##### [状态模式](#14)
  1. [定义](#14.1)
  2. [类图](#14.2)

* ##### [代理模式](#15)
  1. [定义](#15.1)
  2. [远程代理](#15.2)
  3. [保护代理](#15.3)
  4. [同步代理](#15.4)

* ##### [建造者模式(Builder)](#16)
  1. [意图](#16.1)
  2. [类图](#16.2)

* ##### [桥接模式(Bridge)](#17)
  1. [意图](#17.1)
  2. [类图](#17.2)

* ##### [原型模式(Prototype)](#18)
  1. [意图](#18.1)
  2. [类图](#18.2)

* ##### [享元模式(Flyweight)](#19)
  1. [意图](#19.1)
  2. [类图](#19.2)

* ##### [责任链模式(Chain Of Responsibility)](#20)
  1. [意图](#20.1)
  2. [类图](#20.2)

* ##### [解释器模式(Interpreter)](#21)
  1. [意图](#21.1)
  2. [类图](#21.2)

* ##### [中介者模式(Mediator)](#22)
  1. [意图](#22.1)
  2. [类图](#22.2)

* ##### [备忘录模式(Memento)](#23)
  1. [意图](#23.1)
  2. [类图](#23.2)

* ##### [访问者模式(Visitor)](#24)
  1. [意图](#24.1)
  2. [类图](#24.2)

<h3 id="1">面向对象</h3>

<h4 id="1.1">OO特征</h4>

<img src="../assets/images/edraw/oo.png?v=1" width="380">

<h4 id="1.2">OO原则</h4>

<img src="../assets/images/edraw/oo_principle.png?v=2" width="820">

<h4 id="1.3">设计模式一览</h4>

<img src="../assets/images/edraw/design_pattern.png?v=4" width="1000">

<h3 id="2">单例模式(Singleton)</h3>

<h4 id="2.1">意图</h4> 

确保一个类只有一个实例，并提供一个全局访问点。

<h4 id="2.2">类图</h4> 

<img src="../assets/images/edraw/uml_singleton.png?v=1" width="625">

<h4 id="2.3">单例模式VS静态变量</h4>

<img src="../assets/images/edraw/singleton_why.png?v=2" width="750">

<h3 id="3">策略模式</h3>

<h4 id="3.1">定义</h4> 

定义算法族，分别封装起来，让他们之间可以互相替换，此模式让算法的变化独立于使用算法的客户。

<h4 id="3.2">类图</h4> 

以动画时间插值器为例：

<img src="../assets/images/edraw/strategy_uml.png?v=1" width="650">

<h4 id="3.3">应用:TimeInterpolator</h4>

```java
public class ValueAnimator extends Animator implements AnimationHandler.AnimationFrameCallback {

    // The time interpolator to be used if none is set on the animation
    private static final TimeInterpolator sDefaultInterpolator =
            new AccelerateDecelerateInterpolator();

    private TimeInterpolator mInterpolator = sDefaultInterpolator;
    
    @Override
    public void setInterpolator(TimeInterpolator value) {
        if (value != null) {
            mInterpolator = value;
        } else {
            mInterpolator = new LinearInterpolator();
        }
    }

    void animateValue(float fraction) {
        fraction = mInterpolator.getInterpolation(fraction);
        // ...
    }
}
```

<h3 id="4">观察者模式</h3>

<h4 id="4.1">定义</h4> 

定义对象间一对多的依赖，当一个对象改变状态时，它的所有依赖者都会收到通知并自动更新。

<h4 id="4.2">类图</h4> 

以ListView用到的观察者模式为例：

<img src="../assets/images/edraw/uml_observer.png?v=3" width="1000">

<h3 id="5">装饰者模式(Decorator)</h3>

<h4 id="5.1">意图</h4> 

动态地将责任附加到对象上。想要扩展功能，装饰者提供有别于继承的另一种选择。

<h4 id="5.2">类图</h4> 

以InputStream为例：

<img src="../assets/images/edraw/uml_decorator.png?v=1" width="470">

<h3 id="6">工厂方法模式(Factory Method)</h3>

<h4 id="6.1">意图</h4> 

定义一个创建对象的接口，但由子类决定要实例化的类是哪一个。工厂方法让类把实例化延迟到子类。

<h4 id="6.2">类图</h4> 

<img src="../assets/images/edraw/uml_factoryMethod.png?v=1" width="600">

<h4 id="6.3">应用:ThreadFactory</h4> 

```java
public interface ThreadFactory {

    Thread newThread(Runnable r);
    
}
```

```java
    public ThreadPoolExecutor(int corePoolSize,
                              int maximumPoolSize,
                              long keepAliveTime,
                              TimeUnit unit,
                              BlockingQueue<Runnable> workQueue,
                              ThreadFactory threadFactory,
                              RejectedExecutionHandler handler) {
    	// ...
        this.threadFactory = threadFactory;
        // ...
    }
```

<h3 id="7">抽象工厂模式(Abstract Factory)</h3>

<h4 id="7.1">意图</h4> 

提供一个创建一系列相关或相互依赖的对象的接口，而无需指定它们具体的类。

<h4 id="7.2">类图</h4> 

<img src="../assets/images/edraw/uml_abstractFactory.png?v=1" width="900">

<h3 id="8">命令模式</h3>

<h4 id="8.1">定义</h4> 

将请求封装成对象。

<h4 id="8.2">类图</h4> 

以线程池为例：

<img src="../assets/images/edraw/uml_command.png" width="770">

<h4 id="8.3">应用:ThreadPoolExecutor</h4>

```java
public interface Runnable {
    public abstract void run();
}
```
```java
public class ThreadPoolExecutor extends AbstractExecutorService {
    public void execute(Runnable command) {
        // ...
    }
}
```

<h3 id="9">适配器模式(Adapter)</h3>

<h4 id="9.1">意图</h4> 

将一个类的接口，转换成客户期望的另一个接口。适配器让原本不兼容的类可以合作无间。

<h4 id="9.2">类图</h4> 

以ListView为例：

<img src="../assets/images/edraw/uml_adapter.png?v=1" width="600">

<h3 id="10">外观模式(Facade)</h3>

<h4 id="10.1">意图</h4> 

为子系统提供一个接口，便于它的使用。

<h4 id="10.2">类图</h4> 

<img src="../assets/images/edraw/uml_facade.png?v=1" width="660">

<h3 id="11">模板方法模式</h3>

<h4 id="11.1">定义</h4> 

在一个方法中定义一个算法的骨架，而将一些步骤延迟到子类中。模板方法使得子类可以在不改变算法结构的情况下，重新定义算法中的某些步骤。

<h4 id="11.2">类图</h4> 

以View的绘制流程为例：

<img src="../assets/images/edraw/uml_templateMethod.png" width="680">

<h4 id="11.3">应用:View.draw</h4>

```java
    public void draw(Canvas canvas) {
        // draw the background, if needed
        drawBackground(canvas);
        // draw the content
        if (!dirtyOpaque) onDraw(canvas);
        // draw the children
        dispatchDraw(canvas);
    }
```

<h3 id="12">迭代器模式</h3>

<h4 id="12.1">定义</h4> 

封装遍历，提供一种方法顺序访问一个聚合对象中的各个元素，而又不暴露其内部的表示。

<h4 id="12.2">类图</h4> 

以List为例：

<img src="../assets/images/edraw/uml_iterator.png" width="630">

<h3 id="13">组合模式(Composite)</h3>

<h4 id="13.1">意图</h4> 

让客户以一致的方式处理个别对象以及对象组合。

<h4 id="13.2">类图</h4> 

<img src="../assets/images/edraw/uml_composite.png?v=1" width="550">

<h3 id="14">状态模式</h3>

<h4 id="14.1">定义</h4> 

运行对象在内部状态改变时改变它的行为，对象看起来好像修改了它的类。

<h4 id="14.2">类图</h4> 

<img src="../assets/images/edraw/uml_state.png?v=1" width="500">

<h3 id="15">代理模式</h3>

<h4 id="15.1">定义</h4>

为另一个对象提供一个替身或者占位符以控制对这个对象的访问。

<h4 id="15.2">远程代理</h4>

<img src="../assets/images/edraw/uml_aidl.png?v=1" width="850">

<h4 id="15.3">保护代理</h4>

<img src="../assets/images/edraw/uml_protect_proxy.png" width="590">

<h4 id="15.4">同步代理</h4>

<img src="../assets/images/edraw/uml_sync_proxy.png" width="600">

<h3 id="16">建造者模式(Builder)</h3>

<h4 id="16.1">意图</h4> 

将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。

<h4 id="16.2">类图</h4> 

<img src="../assets/images/edraw/uml_builder.png" width="750">

<h3 id="17">桥接模式(Bridge)</h3>

<h4 id="17.1">意图</h4> 

将抽象部分与它的实现部分分离，使它们都可以独立地变化。

<h4 id="17.2">类图</h4> 

<img src="../assets/images/edraw/uml_bridge.png" width="880">

<h3 id="18">原型模式(Prototype)</h3>

<h4 id="18.1">意图</h4> 

用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。

<h4 id="18.2">类图</h4> 

<img src="../assets/images/edraw/uml_prototype.png" width="600">

<h3 id="19">享元模式(Flyweight)</h3>

<h4 id="19.1">意图</h4> 

利用共享技术有效地支持大量细粒度对象。

<h4 id="19.2">类图</h4> 

<h3 id="20">责任链模式(Chain Of Responsibility)</h3>

<h4 id="20.1">意图</h4> 

使多个对象都有机会处理请求，从而避免请求的发送者和接收者直接的耦合关系。

<h4 id="20.2">类图</h4> 

<img src="../assets/images/edraw/uml_responsibility.png" width="500">

<h3 id="21">解释器模式(Interpreter)</h3>

<h4 id="21.1">意图</h4> 

给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。

<h4 id="21.2">类图</h4> 

<h3 id="22">中介者模式(Mediator)</h3>

<h4 id="22.1">意图</h4> 

用一个中介来封装一系列的对象交互。中介者使各个对象不需要显示地相互引用，从而使其耦合松散，而且可以独立地改变他们之间的交互。

<h4 id="22.2">类图</h4> 

<h3 id="23">备忘录模式(Memento)</h3>

<h4 id="23.1">意图</h4> 

在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态，这样以后就可以将该对象恢复到原先保存的状态。

<h4 id="23.2">类图</h4> 

<h3 id="24">访问者模式(Visitor)</h3>

<h4 id="24.1">意图</h4> 

表示一个作用于某对象结构中的各元素的操作。它使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。

<h4 id="24.2">类图</h4> 