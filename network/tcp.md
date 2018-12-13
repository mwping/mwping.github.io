## TCP

#### 特点

* 面向连接
* 点对点(一对一)；
* 可靠交付：无差错、不丢失、不重复、按序到达；
* 全双工；
* 面向字节流；

#### TCP报文段首部格式

![](../assets/images/tcp_header.png?v=2)


**序号**：己方发送的数据的第1个字节的编号。

**确认号**：期望接收对方下一条报文的第1个字节编号。

![](../assets/images/tcp_1.png?v=2)

![](../assets/images/tcp_2.png?v=2)

**数据偏移**

占4位，能够表示的范围是0-15，以4字节为单位，最大偏移60字节，也就是TCP首部的最大长度是60字节。

![](../assets/images/tcp_3.png?v=2)

**保留**

6位，置0。

**Urgent**

紧急标志。

**ACK**

除3次握手的第一次握手ACK标志为0，其他情况下ACK均为1。

![](../assets/images/tcp_4.png?v=2)

**Push**

接收方收到之后尽快交给应用进程，而不再等到整个缓冲区都填满。

**Reset**

复位。

**Syn**

同步，建立连接时使用。

**Fin**

终止，释放连接时使用。

**检验和**

12字节伪首部+TCP首部+数据。例如：

![](../assets/images/tcp_5.png?v=2)

计算方法为：

```java
        long result = ChecksumUtils.getCheckSum(new int[]{
                // 12字节伪首部
                0xc0a8,//源ip前半部分:192.168
                0x0069,//源ip后半部分:0.105
                0xc0a8,//目标ip前半部分:192.168
                0x0065,//目标ip后半部分:0.101
                0x0006,//定值，指TCP协议号
                37, //tcp长度
                // 12字节伪首部 end

                // tcp 首部
                0xe240,// 源端口
                0x07e2,// 目标端口
                0x8b63,
                0x86f0,
                0x1763,
                0x7266,
                0x8018,
                0x1015,
                0x0000,// 检验和初始值0
                0x0000,
                0x0101,
                0x080a,
                0x01ad,
                0x6b83,
                0x006f,
                0xd12d,
                // tcp 首部 end

                0x6162,//数据
                0x6320,//数据
                0x0a00,//数据
        });
```

```java
public class ChecksumUtils {
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
}
```
#### 可靠传输的工作原理

**停止等待协议**

每发送完一个分组就停止发送，等待对方确认，在收到确认后再发送下一个分组。如果分组传输过程中丢失或者出现差错，对方不会发送确认，发送方超过一段时间没有收到确认，就认为刚刚发送的分组丢失，于是重传刚刚的分组，即**超时重传**。停止等待协议效率低，实际上基本不用。

**连续ARQ(Automatic Repeat reQuest)协议**

