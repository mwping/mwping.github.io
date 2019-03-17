
## WebView优化实践

#### 对比数据

|对比|优化|原生|
|:-:|:-:|:-:|
|缓存上限|<font color='green'>无限制，取决于手机存储空间。</font>|<20M|
|首次加载速度(5张大图)|275ms|<font color='green'>258ms</font>|
|首次加载速度(10张大图)|<font color='green'>433ms</font>|491ms|
|磁盘缓存(15M)|414ms|<font color='green'>329ms</font>|
|内存(10张大图)|100-106M|基本持平|
|和原生图片互通有无|<font color='green'>支持</font>|不支持|
