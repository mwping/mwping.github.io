## UDP

#### 特点

* 无连接；
* 尽最大努力交付(不可靠)，应用程序本身可以增加一些提高可靠性的措施；
* 面向报文，应用层交下来的报文，不合并，不拆分，应用层交给UDP多长的报文，UDP就照样发送。应用程序必须选择合适大小的报文，太长会让IP层分片，影响IP层效率；太短会使IP数据报的首部的相对长度太大，也降低IP层效率。
* 没有拥塞控制，主机以恒定的速率发送数据，因此适合允许丢包但是实时性要求高的场景，如IP电话、视频会议；但当很多主机像网络高速率发送UDP数据，可能造成严重的网络拥塞问题；
* 支持一对一、一对多、多对一、多对多的交互；
* 首部开销小，只有8字节，TCP需要20个字节。

#### 抓包分析

1. 源端口：2字节，取值范围[0,65535];
2. 目的端口：2字节，取值范围[0,65535];
3. 长度：2字节，值=头长度+数据长度，假如数据部分长度为10字节，则长度为18(包括头部的8字节)。
4. 检验和：2字节，检测UDP用户数据报在传输中是否有错。有错则丢弃。

例如，使用UDP协议发送字符串"abc"，抓到的数据包如下：

![](../assets/images/udp_capture.png?v=1)

#### 检验和的计算

计算公式(java)
```java
    /**
     * 反码获取检验和
     * 参考：https://baike.baidu.com/item/%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%8F%8D%E7%A0%81%E6%B1%82%E5%92%8C/10462750?fr=aladdin
     *
     * @return
     */
    public static int getCheckSum(int[] data) {
        int sum = 0;
        int n = data.length;
        for (int i = 0; i < n; i++) {
            sum += data[i];
            sum = (sum >> 16) + (sum & 0xffff);
        }
        sum = ~sum;
        sum = sum & 0xffff;
        return sum;
    }
```

**示例：**

上图的检验和计算方法：

```java
    long result = ChecksumUtils.getCheckSum(new int[]{
            0xc0a8,//源ip前半部分:192.168
            0x0069,//源ip后半部分:0.105
            0xc0a8,//目标ip前半部分:192.168
            0x0065,//目标ip后半部分:0.101
            17,//定值，指UDP协议号
            11,//udp长度
            52931,// 源端口
            2020,// 目标端口
            11,//udp长度
            0,//检验和初始值
            0x6162,//数据
            0x6300//数据(不足偶数位补0，0x63->0x6300)
    });
```

得出的结果是：0xe2ae，和抓包中的Checksum值一致。


