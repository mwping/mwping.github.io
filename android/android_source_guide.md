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

