## 理解Java中的锁概念

### 互斥同步

Java编译之后，同步块的前后生成monitorenter、monitorexit字节码指令，这两个指令都需要一个reference对象作为参数来指明要加锁和解锁的对象。

monitorenter指令先要尝试获得对象的锁，如果这个对象没有被锁定，或者已被当前线程获得，锁计数器+1，相应的，monitorexit将计数器-1。计数器0时，锁被释放。如果获取对象锁失败，线程阻塞。

另外，同一个线程，锁可以重入，同一个线程不会自己锁死自己，例如考虑synchronized嵌套的情况：

```java
public class LockDemo {
    private final Object lock = new Object();

    public int get() {
        synchronized (lock) {
            synchronized (lock) {
            }
        }
        return 0;
    }
}
```

### 锁的性能消耗

* 维护锁计数器；
* 检查是否有被阻塞的线程需要唤醒；
* 阻塞或者唤醒线程，需要操作系统帮忙完成，其耗费的处理器时间可能比一般的getter()/setter()方法本身的执行时间还长，所以synchronized属于Java语言中的重量级操作；

### CAS——非阻塞同步

CAS指令需要3个参数：
1. 内存地址；
2. 旧的预期值；
3. 新值；

当且仅当内存地址的当前值符合旧的预期值时，处理器才用新值去更新内存。


### 公平锁

按照申请锁的时间顺序依次获得锁。synchronized非公平，ReentrantLock默认非公平，可以通过构造参数设置为公平锁：

```java
public ReentrantLock(boolean fair)
```

### 自旋锁

假设这样一种情况，第一个线程还剩1ms释放锁，此时第二个线程来尝试获取这个锁，发现锁已经被前一个线程占用，于是操作系统让第二个线程阻塞。刚阻塞完成，发现锁已经被释放了，又去唤醒这个线程，阻塞-唤醒的时间，可能比竞争时间(例如前面说的1ms)还长。

为了1ms的竞争时间去阻塞-唤醒线程，显然得不偿失，自旋锁就是为了优化这种情况。自旋锁可以理解为加了一个空的for/while循环。使用自旋机制，第二个线程发现锁被占用时，虚拟机不去让操作系统阻塞线程，而是让第二个线程执行一个循环，例如自旋10次：
```
    public void spinning() {
        for (int i = 0; i < 10; i++) {
            //
        }
    }
```
自旋完成之后，发现锁已经被释放了，于是就能顺利的获得锁了，避免了阻塞-唤醒过程。（上面的代码是为了模拟自旋概念，实际上自旋操作是在虚拟机层面完成的，必然不是这样的Java代码。）

自适应自旋，就是让自旋机制变得更智能一点。如果某个锁对象自旋10次获得锁成功，那么下一次竞争锁允许它自旋100次。而对于某个锁，如果自旋很少成功获得锁，除了阻塞等待还白白增加了自旋带来的消耗，那么以后获得这个锁时自旋过程可能就被省略。

### 锁消除

锁消除是指虚拟机对一些代码上要求同步，但是检测到不可能存在共享数据竞争的锁进行消除，说白了就是某段Java代码加了synchronized关键字，但是运行时被虚拟机无视。看下面一段代码：
```Java
    public String concatString(String s1, String s2, String s3) {
        StringBuffer buffer = new StringBuffer();
        buffer.append(s1);
        buffer.append(s2);
        buffer.append(s3);
        return buffer.toString();
    }
```

StringBuffer.java的append方法：
```java
    @Override
    public synchronized StringBuffer append(String str) {
        toStringCache = null;
        super.append(str);
        return this;
    }
```

按照一般理解，执行```buffer.append()```时，buffer对象会被锁住，防止其他线程修改buffer的内容。但是实际上buffer作用域是在方法内部，其引用永远不会“逃逸”到方法之外，可以认为是线程私有的，也就是其他线程无法拿到buffer对象的引用从而无法修改其值，因此concatString方法不存在数据竞争问题，所以其内部的```buffer.append()```是没有必要加锁-解锁的，虚拟机检测到这一情况，在执行时就会忽略同步而直接执行。

另外，上面的代码只是为了演示锁消除的例子，实际上应该使用StringBuilder。

### 轻量级锁

轻量级锁是进入同步块时，先检查对象有没有被锁住，如果对象未锁定(Mark Word标志位=01)，首先在当前栈帧创建Lock Record，存放对象头的Mark Word的备份，并使用CAS操作，把对象头的Mark Word替换为该Lock Record的指针，此时的CAS操作三个参数如下：

1. 地址：对象头Mark Word地址；
2. 旧预期值：Lock Record存储的原始Mark Word备份；
3. 新值：Lock Record指针。

**加锁**

如果当前对象头的Mark Word和Lock Record中的备份一致，说明还尚未有其他线程抢先获得锁，则本线程CAS成功，对象头的Mark Word内容变成Lock Record指针，标志位变成00，即轻量级锁定状态，此情况避免了一次操作系统线程调度的发生；

如果当前对象头的Mark Word和Lock Record中的备份不一致，此时对象头存的应该是指向另一个线程的Lock Record指针，而本线程CAS预期的旧值是原始Mark Word，故CAS失败，对象头的Mark Word值改成指向重量级锁(互斥量)的指针，标志位改成10(膨胀，重量级锁定)，该线程及后续线程均要进入阻塞状态。

**解锁**

解锁也使用CAS来完成。如果对象头的Mark Word仍然是指向本线程Lock Record的指针，那么使用CAS把对象头的Mark Word的值替换为Lock Record中存放的原始备份，同步过程完成；

如果CAS失败，说明锁已经膨胀了，对象头的Mark Word已经被改成了指向重量级锁(互斥量)的指针，那么在释放锁的时候，唤醒阻塞的线程。

轻量级锁机制是基于一个经验数据：大多数情况下同步周期内不存在竞争。这种情况下轻量级锁机制能够减少操作系统介入线程同步操作，就像代码本身无需同步一样。

### 偏向锁

偏向锁是在无竞争情况下，相比轻量级锁，连CAS操作都去掉了。

锁对象第一次被线程获取时，使用CAS把获得锁的线程ID记录在对象Mark Word中，如果成功，则该线程以后每次进入这个锁相关的同步块(根据Mark Word记录的线程ID判断)，虚拟机都不再进行任何同步操作，减少加锁解锁的消耗，如维护锁计数器、检查是否有待唤醒的线程等。

如果另一个线程尝试获得这个锁，如果前一个偏向锁的线程已经结束了，那么重新偏向这个新的线程，如果此时前一个线程仍存在但是已经释放了锁，则撤销偏向模式；如果此时另一个线程还占有这个锁，那么偏向锁升级为轻量级锁：为已占用锁的线程创建Lock Record，复制Mark Word，CAS把对象头Mark Word改为执行Lock Record的指针，接下来的流程就跟上面的轻量级锁一致了。





