## 待办事项

#### 查看jdk安装目录

```
$ /usr/libexec/java_home -V
Matching Java Virtual Machines (1):
    1.8.0_73, x86_64:	"Java SE 8"	/Library/Java/JavaVirtualMachines/jdk1.8.0_73.jdk/Contents/Home
```

#### 查看gradle依赖树
```
./gradlew 模块名:dependencies
```

#### Git 添加子模块
```
git submodule add https://xxx/xxx.git my/dir
```

#### Github太慢解决方案

1.查询github.com地址:[http://tool.chinaz.com/dns/?type=1&host=github.com&ip=](http://tool.chinaz.com/dns/?type=1&host=github.com&ip=)

2.使用ping找出最快的ip地址
```
ping 192.30.255.112
```

3.找到hosts文件
```
cd /private/etc/
open .
```
4.增加一行
```
192.30.255.112	github.com
```