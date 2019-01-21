## Handler机制分析

### 目录

* ##### [框架图](#1)

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