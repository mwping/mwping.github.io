## ReactNative原生和JS通信原理

参考文档：

1. [React Native模块加载与原理分析](https://www.jianshu.com/p/af4cb096785b)
2. [React Native通信原理源码分析一](https://www.jianshu.com/p/ccab1a94b637)
3. [React Native通信原理源码分析二](https://www.jianshu.com/p/4c4e08211d83)

**方法调用**

1.每个Module被一个JavaModuleWrapper管理；

2.JavaModuleWrapper通过findMethods方法，找到带ReactMethod注解的方法，存放在List中(mMethods)；

3.每个方法使用一个JavaMethodWrapper管理；

4.JS调用原生方法，最后使用的是反射；

JavaMethodWrapper.java
```java
mMethod.invoke(mModuleWrapper.getModule(), mArguments);
```