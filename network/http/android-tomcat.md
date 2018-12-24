## 基于Tomcat调试Android http/https

### 目录

* ##### [配置Tomcat](#1)
  1. [下载](#1.1)
  2. [启动](#1.2)
  3. [停止](#1.3)

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


