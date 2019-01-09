## App构建流程分析

### 目录

* ##### [构建流程](#1)
  1. [官方文档](#1.1)

* ##### [流程分析](#2)
  1. [配置源码](#2.1)
  2. [找到插件主类](#2.2)

<h3 id="1">构建流程</h3>

<h4 id="1.1">官方文档</h4> 

[Configure your build](https://developer.android.com/studio/build/)

![](../assets/images/build-process_2x.png)

(原图地址:https://developer.android.com/images/tools/studio/build-process_2x.png)


<h3 id="2">流程分析</h3>

<h4 id="2.1">配置源码</h4> 

新建项目，添加依赖:
```
dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])
    implementation 'com.android.support:appcompat-v7:28.0.0'
    implementation 'com.android.support.constraint:constraint-layout:1.1.3'
    implementation 'com.android.tools.build:gradle:3.2.1' // add this line
}
```
sync gradle之后效果如下：

![](../assets/images/gradle321.png)

<h4 id="2.2">找到插件主类</h4> 

app/build.gradle一般是这样开头：
```
apply plugin: 'com.android.application'
```
通过插件名找到主类`AppPlugin.java`

![](../assets/images/appplugin.png)

```java
/** Gradle plugin class for 'application' projects, applied on the base application module */
public class AppPlugin extends AbstractAppPlugin {
    // ...
}
```