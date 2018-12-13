## adb调试

[https://developer.android.com/studio/command-line/adb](https://developer.android.com/studio/command-line/adb)

### adb push

将文件文件或目录（及其子目录）复制到模拟器或设备:

```
adb push local remote
```
在上述命令中，local 和 remote 指的是开发计算机（本地）和模拟器/设备实例（远程）上目标文件/目录的路径。例如：
```
adb push foo.txt /sdcard/foo.txt
```
