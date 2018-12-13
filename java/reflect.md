## 自定义类加载器和反射调用

### 自定义类加载器

**一般步骤**

1. 创建类，继承ClassLoader;
2. 定义.class文件路径；
3. 重写findClass方法；
4. 获取字节流(byte[])。

```java
package com.github.mwping.classloadsample;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

public class MyClassLoader extends ClassLoader {
    public static final String dir = "/Users/mengweiping/Github/Java/TargetClassSample/src/com/github/mwping/target/";
    public static final String fileType = ".class";

    public Class<?> findClass(String name) {
        byte[] b = loadClassData(name);
        return defineClass(null, b, 0, b.length);
    }

    private byte[] loadClassData(String name) {
        FileInputStream fis = null;
        byte[] data = null;
        try {
            File file = new File(dir + name + fileType);
            fis = new FileInputStream(file);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            int ch = 0;
            while ((ch = fis.read()) != -1) {
                baos.write(ch);
            }
            data = baos.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (fis != null) {
                try {
                    fis.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return data;
    }
}

```

### 定义类
```java
package com.github.mwping.target;

public class Target {

    public static String staticName = "static_name";
    private static String privateStaticName = "private_static_name";
    /**
     * 类静态代码块
     */
    static {
        System.out.println("I'm Target class, staticName = " + staticName);
    }

    /**
     * 实例代码块
     */
    {
        System.out.println("I'm Target instance.");
    }

    public static int add(int i, int j) {
        return i + j;
    }

    private static int multiple(int i, int j) {
        return i * j;
    }

    private int id = 2018;

    public String name = "default";

    public Target() {
    }

    public Target(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }
    
    private void setId(int id) {
        this.id = id;
    }

    public static String getPrivateStaticName() {
        return privateStaticName;
    }
}
```

### 编译

生成.class文件，放到自定义类加载器指定目录。

```
javac Target.java
```

### 加载类

```java
    MyClassLoader loader = new MyClassLoader();
    Class<?> targetClass = loader.loadClass("Target");
```

### 反射调用

反射调用可以实现：

* 读/写public/private静态变量
* 无参/有参构造器创建实例
* 读/写实例public/private变量
* 调用静态public/private方法
* 调用实例public/private方法

```java
package com.github.mwping.classloadsample;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Main {

    public static void main(String[] args) {
        MyClassLoader loader = new MyClassLoader();
        invokeTarget(loader);
    }

    private static void invokeTarget(MyClassLoader loader) {
        try {
            /**
             * 加载类
             */
            Class<?> targetClass = loader.loadClass("Target");

            /**
             * 读public静态变量
             */
            Field publicStaticField = targetClass.getField("staticName");
            String staticName = (String) publicStaticField.get(null);
            System.out.println("getField \"staticName\", value = " + staticName);

            /**
             * 写public静态变量
             */
            publicStaticField.set(null, staticName + 2018);
            staticName = (String) publicStaticField.get(null);
            System.out.println("getField \"staticName\" after set, value = " + staticName);

            /**
             * 读private静态变量
             */
            Field staticPrivateField = targetClass.getDeclaredField("privateStaticName");
            staticPrivateField.setAccessible(true);
            String privateStaticName = (String) staticPrivateField.get(null);
            System.out.println("getField \"privateStaticName\", value = " + privateStaticName);

            staticPrivateField.set(null, privateStaticName + 2018);
            privateStaticName = (String) staticPrivateField.get(null);
            System.out.println("getField \"privateStaticName\" after set, value = " + privateStaticName);

            /**
             * 无参构造器创建实例
             */
            Object target = targetClass.newInstance();

            /**
             * 有参构造器创建实例
             */
            Constructor<?> constructor = targetClass.getConstructor(int.class);
            target = constructor.newInstance(1999);

            /**
             * 读实例public变量
             */
            Field nameField = targetClass.getDeclaredField("name");
            String name = (String) nameField.get(target);
            System.out.println("getField \"name\", value = " + name);
            /**
             * 写实例public变量
             */
            nameField.set(target, "mwping");
            name = (String) nameField.get(target);
            System.out.println("getField \"name\", value = " + name);

            /**
             * 读实例private变量
             */
            Field privateField = targetClass.getDeclaredField("id");
            privateField.setAccessible(true);
            int id = (int) privateField.get(target);
            System.out.println("getField \"id\", value = " + id);
            /**
             * 写实例private变量
             */
            privateField.set(target, 2018);
            id = (int) privateField.get(target);
            System.out.println("getField \"id\", value = " + id);

            /**
             * 调用静态public方法
             */
            Method publicStaticMethod = targetClass.getMethod("add", int.class, int.class);
            // 静态方法第一个参数只需传null
            int result = (int) publicStaticMethod.invoke(null, 4, 5);
            System.out.println("invoke \"add\" method, result = " + result);

            /**
             * 调用静态private方法
             */
            Method privateStaticMethod = targetClass.getDeclaredMethod("multiple", int.class, int.class);
            privateStaticMethod.setAccessible(true);
            // 静态方法第一个参数只需传null
            result = (int) privateStaticMethod.invoke(null, 4, 5);
            System.out.println("invoke \"multiple\" method, result = " + result);

            /**
             * 调用实例public方法
             */
            Method publicMethod = targetClass.getMethod("getId");
            id = (int) publicMethod.invoke(target);
            System.out.println("invoke \"getId\" method, id = " + id);

            /**
             * 调用实例private方法
             */
            Method privateMethod = targetClass.getDeclaredMethod("setId", int.class);
            privateMethod.setAccessible(true);
            privateMethod.invoke(target, 1234);
            id = (int) publicMethod.invoke(target);
            System.out.println("after invoke \"setId\" method, id = " + id);

        } catch (ClassNotFoundException | NoSuchFieldException | SecurityException | IllegalArgumentException
                | IllegalAccessException | InstantiationException | NoSuchMethodException
                | InvocationTargetException e) {
            e.printStackTrace();
        }
    }
}
```

输出：
```
I'm Target class, staticName = static_name
getField "staticName", value = static_name
getField "staticName" after set, value = static_name2018
getField "privateStaticName", value = private_static_name
getField "privateStaticName" after set, value = private_static_name2018
I'm Target instance.
I'm Target instance.
getField "name", value = default
getField "name", value = mwping
getField "id", value = 1999
getField "id", value = 2018
invoke "add" method, result = 9
invoke "multiple" method, result = 20
invoke "getId" method, id = 2018
after invoke "setId" method, id = 1234
```

### Android中的反射

Android需要用DexClassLoader来完成自定义类加载，接下来的反射调用就和Java的一样了。
```java
        DexClassLoader loader = new DexClassLoader(
                file.getAbsolutePath(),//apk文件路径
                getDir("dex", Context.MODE_PRIVATE).getAbsolutePath(),
                null,//不涉及.so文件的话，传null即可
                getClassLoader());//双亲委派
        Class<?> targetClass = loader.loadClass("com.github.mwping.pluggableclientapp.MainActivity");
```
