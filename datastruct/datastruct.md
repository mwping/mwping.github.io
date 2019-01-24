## 图解数据结构

### 目录

* ##### [ArrayMap](#1)
  1. [设计目的](#1.1)
  2. [图解](#1.2)
  3. [使用场景](#1.3)

<h3 id="1">ArrayMap</h3>

<h4 id="1.1">设计目的</h4> 

more memory efficient，比HashMap更省内存，但是查找效率比HashMap低，时间换空间。

<h4 id="1.2">图解</h4> 

使用两个数组，一个int数组存放每个Item的hash值，一个Object数组存放键值对：
```java
    int[] mHashes;
    Object[] mArray;
```

![](../assets/images/edraw/ArrayMap.png)

<h4 id="1.3">使用场景</h4> 

因为数组的插入、删除、扩容效率低，ArrayMap适应的场景：

1. <1000对象；
2. Map嵌套；