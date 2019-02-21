## App构建流程分析

### 目录

* ##### [构建流程简介](#1)
  1. [官方文档](#1.1)

* ##### [构建流程探析](#2)
  1. [Demo地址](#2.1)
  2. [生成gradle报告](#2.2)

<h3 id="1">构建流程简介</h3>

<h4 id="1.1">官方文档</h4> 

[Configure your build](https://developer.android.com/studio/build/)

<img src="../assets/images/build-process_2x.png" width="500">

(原图地址:https://developer.android.com/images/tools/studio/build-process_2x.png)

<h3 id="2">构建流程探析</h3>

<h4 id="2.1">Demo地址</h4> 

[https://github.com/mwping/build-apk-analysis](https://github.com/mwping/build-apk-analysis)

<h4 id="2.2">生成gradle报告</h4> 

```
./gradlew assembleDebug --scan
...
BUILD SUCCESSFUL in 2s
25 actionable tasks: 5 executed, 20 up-to-date

Publishing a build scan to scans.gradle.com requires accepting the Gradle Terms of Service defined at https://gradle.com/terms-of-service. Do you accept these terms? [yes, no]
yes
Gradle Terms of Service accepted.

Publishing build scan...
https://gradle.com/s/kh2uq2j6lg4cw
```
打开timeline：[https://scans.gradle.com/s/kh2uq2j6lg4cw/timeline](https://scans.gradle.com/s/kh2uq2j6lg4cw/timeline)






