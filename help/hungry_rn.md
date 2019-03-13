## ReactNative

#### CodePush

参考文档：

* [Microsoft Android CodePush](https://github.com/Microsoft/react-native-code-push/blob/master/docs/setup-android.md#plugin-installation-android---rnpm)
* [Code Push 热更新使用详细说明和教程](http://bbs.reactnative.cn/topic/725/code-push-%E7%83%AD%E6%9B%B4%E6%96%B0%E4%BD%BF%E7%94%A8%E8%AF%A6%E7%BB%86%E8%AF%B4%E6%98%8E%E5%92%8C%E6%95%99%E7%A8%8B)
* [React Native应用部署/热更新-CodePush最新集成总结(新)](https://blog.csdn.net/qq_33323251/article/details/79437932)

**安装**
```
sudo npm install -g code-push-cli
```
查看版本号：
```
code-push -v
2.1.9
```

**注册**
```
code-push register
```
命令会唤起浏览器，根据引导操作，浏览器中最后出现:
```
Authentication succeeded
Please copy and paste this token to the command window:
2a8703e6e88f073b3fd94b526c08b8a166e5af1a
After doing so, please close this browser tab.
```

复制token，填入到命令行窗口，注册流程命令行窗口看起来如下：
```
$ code-push register
Please login to Mobile Center in the browser window we've just opened.

Enter your token from the browser:  2a8703e6e88f073b3fd94b526c08b8a166e5af1a

Successfully logged-in. Your session file was written to /Users/lixiang/.code-push.config. You can run the code-push logout command at any time to delete this file and terminate your session.
```

**access-key管理**

查看access-key相关命令的用法
```
$ code-push access-key
Usage: code-push access-key <command>

命令：
  add     Create a new access key associated with your account
  remove  Remove an existing access key
  rm      Remove an existing access key
  list    List the access keys associated with your account
  ls      List the access keys associated with your account

选项：
  -v, --version  显示版本号  [布尔]
```
查看access-key列表
```
$ code-push access-key list
┌────────────────────────────┬───────────────┐
│ Name                       │ Created       │
├────────────────────────────┼───────────────┤
│ lixiangdeMacBook-Pro.local │ 6 minutes ago │
└────────────────────────────┴───────────────┘
```

**注册App**
```
$ code-push app add AwesomeProject android react-native
Successfully added the "AwesomeProject" app, along with the following default deployments:
┌────────────┬──────────────────────────────────────────────────────────────────┐
│ Name       │ Deployment Key                                                   │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ Production │ FC0Lp9xdjIrC9XswRtxDoxGzUiWPbe138b39-272a-4281-adfc-7bb4236f97eb │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ Staging    │ WwTPOeoXb9UH_mVmAVrq26vBilJybe138b39-272a-4281-adfc-7bb4236f97eb │
└────────────┴──────────────────────────────────────────────────────────────────┘
```
可以查看已注册的App
```
$ code-push app list
┌────────────────┬─────────────────────┐
│ Name           │ Deployments         │
├────────────────┼─────────────────────┤
│ AwesomeProject │ Production, Staging │
└────────────────┴─────────────────────┘
```

查询key：
```
$ code-push deployment ls AwesomeProject -k
┌────────────┬──────────────────────────────────────────────────────────────────┬─────────────────────┬──────────────────────┐
│ Name       │ Deployment Key                                                   │ Update Metadata     │ Install Metrics      │
├────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┼──────────────────────┤
│ Production │ FC0Lp9xdjIrC9XswRtxDoxGzUiWPbe138b39-272a-4281-adfc-7bb4236f97eb │ No updates released │ No installs recorded │
├────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┼──────────────────────┤
│ Staging    │ WwTPOeoXb9UH_mVmAVrq26vBilJybe138b39-272a-4281-adfc-7bb4236f97eb │ No updates released │ No installs recorded │
└────────────┴──────────────────────────────────────────────────────────────────┴─────────────────────┴──────────────────────┘
```

**集成CodePush SDK**

进入项目目录，执行安装命令：
```
cd Mwp/Github/AndroidCourse/react-native/AwesomeProject/
sudo npm install --save react-native-code-push
```

接下来执行：
```
react-native link react-native-code-push
```

#### 检查更新

检查更新的时机：

1. App每次启动(默认)；
2. App每次切到前台；
3. 用户点击检查更新；

```java
    /**
     * Indicates when you would like to check for (and install) updates from the CodePush server.
     */
    enum CheckFrequency {
        /**
         * When the app is fully initialized (or more specifically, when the root component is mounted).
         */
        ON_APP_START,

        /**
         * When the app re-enters the foreground.
         */
        ON_APP_RESUME,

        /**
         * Don't automatically check for updates, but only do it when codePush.sync() is manully called inside app code.
         */
        MANUAL
    }
```
生效策略：

1. 下次启动生效(默认)；
2. 实时生效；
3. 下次切换到前台时生效；
4. 切后台时生效；

#### 发布更新

**发布强制更新**
```
code-push release-react AwesomeProject android -m --description "测试强制更新"
```

**发布非强制更新**
```
code-push release-react AwesomeProject android --description "测试强制更新"
```

查看更新历史
```
code-push deployment history AwesomeProject Staging
```


