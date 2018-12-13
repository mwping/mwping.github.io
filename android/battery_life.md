## 电池寿命

### 参考文档

[https://developer.android.com/topic/performance/power/](https://developer.android.com/topic/performance/power/)

### 省电主要思想

* **Reduce**(减少)
* **Defer**(延迟)
* **Coalesce**(合并)

### 电量问题分析

* **使用Battery Historian**

官方文档
1. [https://developer.android.com/topic/performance/power/battery-historian](https://developer.android.com/topic/performance/power/battery-historian)
2. [https://github.com/google/battery-historian](https://github.com/google/battery-historian)

**注意官方Github文档关于docker的命令需要改动才能运行：**

```
docker run -p 8812:9999 gcr.io/android-battery-historian/stable:3.0 --port 9999
```
成功之后，浏览器输入：http://localhost:8812/

命令行输入：
```
adb bugreport bugreport.zip
```
成功之后会在PC本地生成bugreport.zip文件，打开[http://localhost:8812/](http://localhost:8812/)，上传bugreport.zip文件，上传完成之后应该是这个界面：
![](../assets/images/battery_historian.png?v=1)

从报表中可以看到电量使用的场景，例如有几个Service在耗电：
![](../assets/images/battery_historian_service.png?v=1)


可以使用命令清除历史数据，重新统计：
```
adb shell dumpsys batterystats --reset
```

### 电量优化策略

* **使用JobScheduler，例如可以设置在充电的情况下执行任务：**

```java
        /**
         * Specify that to run this job, the device needs to be plugged in. This defaults to
         * false.
         * @param requiresCharging Whether or not the device is plugged in.
         */
        public Builder setRequiresCharging(boolean requiresCharging) {
            mConstraintFlags = (mConstraintFlags&~CONSTRAINT_FLAG_CHARGING)
                    | (requiresCharging ? CONSTRAINT_FLAG_CHARGING : 0);
            return this;
        }
```

* **在合适的时机禁止收听广播**

禁止收听静态注册广播，注意这个会一直生效，需要注意启用。

```java
        PackageManager pm = getPackageManager();
        pm.setComponentEnabledSetting(
                new ComponentName(this, MyBroadCastReceiver.class),
                isChecked ? PackageManager.COMPONENT_ENABLED_STATE_DISABLED
                        : PackageManager.COMPONENT_ENABLED_STATE_ENABLED,
                PackageManager.DONT_KILL_APP);
```

注册/取消注册动态广播
```java
    @Override
    protected void onResume() {
        super.onResume();
        registerReceiver(receiver, filter);
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(receiver);
    }
```

可以使用adb命令模拟广播发送，更多命令参考：[https://developer.android.com/studio/command-line/adb](https://developer.android.com/studio/command-line/adb)
```
adb shell am broadcast -a com.github.mwping.broadcastnotify
```

* **警惕大量动画**
* **定位精度越高，电量损耗越大，及时注销定位监听**
* **警惕WakeLock唤醒屏幕**
* **缓存取代重复下载**
* **请求网络数据前先判断网络**
* **可以使用AlarmManager进行定时任务**




