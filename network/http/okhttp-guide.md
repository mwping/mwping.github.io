## okhttp指南

### 目录

* ##### [关于OkHttp](#1)
  1. [GitHub地址](#1.1)

* ##### [Http知识](#2)

* ##### [Http优化](#3)

<h3 id="1">关于OkHttp</h3>

<h4 id="1.1">GitHub地址</h4> 
[https://github.com/square/okhttp](https://github.com/square/okhttp)

<h3 id="2">Http知识</h3>

http/1.0 每次请求需要三报文握手、四报文分手，加上tcp本身的拥塞控制机制如慢启动，效率很低。

http/1.1 默认使用keep-alive=true来为TCP连接保活(例如5分钟)，期间如果有新http请求，不需要重新建立TCP连接。

<h3 id="3">Http优化</h3>

[RealConnection.java](https://github.com/square/okhttp/blob/cdacead7fa826e00825443ebb4dc71f48dd35f4c/okhttp/src/main/java/okhttp3/internal/connection/RealConnection.java)的isEligible方法的注释中提供了关于优化http的两篇文章：

* [Optimizing Application Delivery](https://hpbn.co/optimizing-application-delivery/#eliminate-domain-sharding)
* [HTTP/2 CONNECTION COALESCING](https://daniel.haxx.se/blog/2016/08/18/http2-connection-coalescing/)