## 安全

### 参考文档

[https://developer.android.com/topic/security/best-practices](https://developer.android.com/topic/security/best-practices)

### 安全建议

#### **WebView安全**

* 可以建立一个白名单机制，禁止跳转到不受控制的外部网址。
* 没有必要不要开启setJavaScriptEnabled()

#### **权限安全**

* 如果可以，使用通用Intent取代申请权限，例如创建日历事件。

#### **数据存储安全**

* 尽量使用App私有存储目录，访问这里的数据不需要额外申请权限，且随App卸载而被清除。

```java
// Creates a file with this name, or replaces an existing file
// that has the same name. Note that the file name cannot contain
// path separators.
final String FILE_NAME = "sensitive_info.txt";
String fileContents = "This is some top-secret information!";

FileOutputStream fos = openFileOutput(FILE_NAME, Context.MODE_PRIVATE);
fos.write(fileContents.getBytes());
fos.close();
```

```java
// The file name cannot contain path separators.
final String FILE_NAME = "sensitive_info.txt";
FileInputStream fis = openFileInput(FILE_NAME);

// available() determines the approximate number of bytes that can be
// read without blocking.
int bytesAvailable = fis.available();
StringBuilder topSecretFileContents = new StringBuilder(bytesAvailable);

// Make sure that read() returns a number of bytes that is equal to the
// file's size.
byte[] fileBuffer = new byte[bytesAvailable];
while (fis.read(fileBuffer) != -1) {
    topSecretFileContents.append(fileBuffer);
}
```

* **外部存储目录数据合法性校验**

例如可以进行MD5校验：
```java
DigestUtils.md5Hex(byte[] data)
```

* **只存储非敏感数据**

* **SharedPreferences使用私有模式(MODE_PRIVATE)访问**

#### **用户敏感数据处理**

* 尽量不要存储或者传输用户敏感数据，考虑是否能使用不可逆的数据格式存储，例如不存邮箱地址，而存储其hash值。尽可能减少对用户数据的访问也有助于简化合规工作。


#### **Service安全**

* 没有必要不要使用android:exported=true；
* 声明android:permission属性，使调用者必须在Manifest文件中声明对应的\<uses-permission\>；

#### **BroadcastReceiver**
* 广播接收器默认是导出的，其他应用可以向接收器发送广播，需要添加权限防止任意应用来发送广播；

#### **代码混淆**

#### **校验AppSHA1签名防二次打包**

