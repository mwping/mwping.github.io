## 基于Tomcat调试Android http/https

### 目录

* ##### [配置Tomcat](#1)
  1. [下载](#1.1)
  2. [启动](#1.2)
  3. [停止](#1.3)

* ##### [配置服务器证书](#2)
  1. [创建keystore](#2.1)
  2. [查询keystore](#2.2)
  

<h3 id="1">配置Tomcat</h3>

<h4 id="1.1">下载</h4> 
进入tomcat官网：[http://tomcat.apache.org/](http://tomcat.apache.org/)，找到下载链接，点击下载，下载完成双击解压即可。
![](../../assets/images/tomcat/download.png)

<h4 id="1.2">启动</h4> 
进入解压目录的bin文件夹。
```
$ cd /Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14/bin/
$ sudo sh startup.sh
Password:
Using CATALINA_BASE:   /Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14
Using CATALINA_HOME:   /Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14
Using CATALINA_TMPDIR: /Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14/temp
Using JRE_HOME:        /Library/Java/JavaVirtualMachines/jdk1.8.0_73.jdk/Contents/Home
Using CLASSPATH:       /Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14/bin/bootstrap.jar:/Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14/bin/tomcat-juli.jar
Tomcat started.
```

浏览器正常打开[http://localhost:8080/](http://localhost:8080/)，则说明配置成功：

![](../../assets/images/tomcatlocaltest.png)

<h4 id="1.3">停止</h4> 

```
$ sudo sh shutdown.sh
```

<h3 id="2">配置服务器证书</h3>

<h4 id="2.1">创建keystore</h4> 

进入jdk安装路径的bin目录
```
Last login: Mon Dec 24 23:58:32 on ttys000
localhost:~ lixiang$ /usr/libexec/java_home -V
Matching Java Virtual Machines (1):
    1.8.0_73, x86_64: "Java SE 8" /Library/Java/JavaVirtualMachines/jdk1.8.0_73.jdk/Contents/Home

/Library/Java/JavaVirtualMachines/jdk1.8.0_73.jdk/Contents/Home
$ cd /Library/Java/JavaVirtualMachines/jdk1.8.0_73.jdk/Contents/Home/bin/
```
生成keystore
```
$ keytool -genkeypair -alias mwpingart01 -keyalg RSA -keystore /Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14/conf/keystore/mwpingart.keystore
输入密钥库口令:  
再次输入新口令: 
您的名字与姓氏是什么?
  [Unknown]:  mwping.art
您的组织单位名称是什么?
  [Unknown]:  mwping.art
您的组织名称是什么?
  [Unknown]:  mwping.art
您所在的城市或区域名称是什么?
  [Unknown]:  hz
您所在的省/市/自治区名称是什么?
  [Unknown]:  zj
该单位的双字母国家/地区代码是什么?
  [Unknown]:  ZH
CN=mwping.art, OU=mwping.art, O=mwping.art, L=hz, ST=zj, C=ZH是否正确?
  [否]:  y

输入 <mwpingart01> 的密钥口令
  (如果和密钥库口令相同, 按回车):  
```
可以使用同样的方法，在mwpingart.keystore添加一个新的密钥对(alias=mwpingart02)。

<h4 id="2.2">查询keystore</h4> 

```
$ keytool -list -keystore /Users/lixiang/Mwp/Github/mwping/download/tomcat/apache-tomcat-9.0.14/conf/keystore/mwpingart.keystore 
输入密钥库口令:  

密钥库类型: JKS
密钥库提供方: SUN

您的密钥库包含 2 个条目

mwpingart02, 2018-12-25, PrivateKeyEntry, 
证书指纹 (SHA1): CF:8E:9F:5D:E5:01:C1:C2:89:2A:94:F4:CE:FB:6B:A0:6B:74:14:58
mwpingart01, 2018-12-25, PrivateKeyEntry, 
证书指纹 (SHA1): 7A:04:F7:BE:20:1B:D2:8E:A7:E8:8C:37:50:93:A1:A0:2F:6F:48:BE
```