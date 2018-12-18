---
layout: default
---

## Android源码阅读指南

### 源码下载
1. 清华大学开源软件镜像站 [https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/](https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/)
2. 根据提示，下载 [https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar](https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar)
3. 根据[https://blog.csdn.net/u010963246/article/details/71480684](https://blog.csdn.net/u010963246/article/details/71480684) 、[https://source.android.com/setup/build/initializing#creating-a-case-sensitive-disk-image](https://source.android.com/setup/build/initializing#creating-a-case-sensitive-disk-image) 创建磁盘镜像
```
	hdiutil create -type SPARSE -fs 'Case-sensitive Journaled HFS+' -size 40g ~/android.dmg
	hdiutil resize -size \<new-size-you-want\>g ~/android.dmg.sparseimage
```

4. 根据 [https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/](https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/) 执行repo sync
```
$ cd /Volumes/Android/aosp/
$ repo sync
.....
Fetching projects: 100% (592/592), done.  
Syncing work tree: 100% (592/592), done.  
```

### repo操作帮助

**参考文档**

* [https://source.android.com/setup/develop](https://source.android.com/setup/develop)
* [https://source.android.com/setup/develop/repo](https://source.android.com/setup/develop/repo)

**查看远程分支**
```
$ cd /Volumes/Android/aosp/
$ cd .repo/manifests
$ git branch -a | cut -d / -f 3
* default
android-8.0.0_r17 -> origin
android-8.1.0_r23 -> origin
android-8.1.0_r9 -> origin
master -> origin
...
```
**列出项目及对应目录**
```
$ repo list
...
frameworks/base : platform/frameworks/base
...
```

**查询某个项目的分支**
```
$ repo branch frameworks/base
   (no branches)
```

**检出分支**
```
$ repo start master --all
Starting master: 100% (592/592), done. 
```

**再次查询某个项目的分支**
```
$ repo branch frameworks/base
*  master                    | in all projects
```

### 查找aidl生成的java类

例如查找ActivityManagerService对应的IActivityManager.java、PackageManagerService对应的IPackageManager.java：

```java
public class ActivityManagerService extends IActivityManager.Stub
        implements Watchdog.Monitor, BatteryStatsImpl.BatteryCallback {
}
```


```java
public class PackageManagerService extends IPackageManager.Stub
        implements PackageSender {
}
```
使用命令行进行查找：
```
$ cd /Volumes/Android/aosp/out/target/common/obj/JAVA_LIBRARIES/framework_intermediates/
$ find . -name "IActivityManager.java" -or -name "IPackageManager.java"
./core/java/android/app/IActivityManager.java
./core/java/android/content/pm/IPackageManager.java
```

其实阅读源码不一定非要找到aidl生成的java文件，找到aidl即可：

```
$ cd /Volumes/Android/aosp/frameworks/base
$ find . -name "IActivityManager.aidl" -or -name "IPackageManager.aidl"
./core/java/android/app/IActivityManager.aidl
./core/java/android/content/pm/IPackageManager.aidl
```

