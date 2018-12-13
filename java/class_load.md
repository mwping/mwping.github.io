## 理解类加载机制

### 类加载机制

虚拟机把描述类的数据从Class文件加载到内存，并对数据进行校验、转换解析和初始化，最终形成可以被虚拟机直接使用的Java类型。

### 整体流程

加载->验证->准备->解析->初始化

### 初始化时机

1. **遇到new、getstatic、putstatic、invokestatic四条指令时，如果类没有进行过初始化，则需要先触发其初始化，具体场景是：**

* new：对应常规的new关键字创建对象；
* getstatic：读一个类的静态非final字段值；
* putstatic：修改一个类的静态字段值；
* invokestatic：调用类的静态方法；

代码示例
```java
public class Main {

    public void test() {
        //new
        Simple simple = new Simple();
        //getstatic
        int i = Simple.sIndex;
        //putstatic
        Simple.sIndex = 1;
        //invokestatic
        int j = Simple.getIndex();
    }

    static class Simple {
        static int sIndex = 0;

        static int getIndex() {
            return sIndex;
        }
    }
}
```
对应的字节码：
```
public void test();
    descriptor: ()V
    flags: ACC_PUBLIC
    Code:
      stack=2, locals=4, args_size=1
         0: new           #2                  // class com/github/mwping/lordhelperapp/jvm/Main$Simple
         3: dup
         4: invokespecial #3                  // Method com/github/mwping/lordhelperapp/jvm/Main$Simple."<init>":()V
         7: astore_1
         8: getstatic     #4                  // Field com/github/mwping/lordhelperapp/jvm/Main$Simple.sIndex:I
        11: istore_2
        12: iconst_1
        13: putstatic     #4                  // Field com/github/mwping/lordhelperapp/jvm/Main$Simple.sIndex:I
        16: invokestatic  #5                  // Method com/github/mwping/lordhelperapp/jvm/Main$Simple.getIndex:()I
        19: istore_3
        20: return
```


2. **对类进行反射调用时，如果类没有进行过初始化，则需要先触发其初始化。**

3. **当初始化一个类的时候，如果发现其父类还没有进行过初始化，则需要先触发其父类的初始化。**

4. **虚拟机启动时，先初始化主类(包含public static void main(String [] args)方法的那个类)。**

### 加载

1. 通过类的全限定名来获取定义此类的二进制流；
2. 将字节流所代表的静态存储结构转化为方法区的运行时数据结构；
3. 在内存中生成一个代表这个类的java.lang.Class对象，作为方法区这个类的各种数据的访问入口。

### 验证

**字节流验证——文件格式**

1. 魔数为0xCAFEBABE；
2. 主次版本号是否在当前虚拟机的处理范围；

**元数据验证——语法规范**

1. 是否有父类；
2. 是否继承了final类；
3. 如果不是抽象类，是否实现了父类或者接口要求实现的方法；
4. 是否覆盖了父类的final字段、方法；

**字节码验证**

1. 类型转换是否有效；
2. 指令不会跳转到方法体之外；

**符号引用验证**

1. 是否能根据全限定名找到对应的类；
2. 是否访问了不存在的字段、方法；
3. 是否访问了无权访问的其他类的字段、方法(如private)；

### 准备

为所有类变量(即```static```变量)分配内存并设置初始值，例如int初始值为0，引用类型初始值为null，bool初始值为false。对于```static final```常量，初始值赋值为指定的值，具体看下面的代码：

```java
    public static int value = 123;
```
上面的代码准备阶段完成之后，value值是0而非123；
```java
    public static final int value = 123;
```
上面的代码准备阶段完成之后，value值是123。

### 解析

解析是将常量池的符号引用替换为直接引用的过程。

**符号引用**

什么是符号引用？看下面的代码：
```java
public class Main {
    public void test() {
        Simple.id = 123;
    }

    static class Simple {
        static int id;
    }
}
```
其对应的字节码指令：
```
  public void test();
    descriptor: ()V
    flags: ACC_PUBLIC
    Code:
      stack=1, locals=1, args_size=1
         0: bipush        123
         2: putstatic     #2                  // Field com/github/mwping/lordhelperapp/jvm/Main$Simple.id:I
         5: return
      LineNumberTable:
        line 5: 0
        line 6: 5
```

其中putstatic指令的参数#2，也就是```Field com/github/mwping/lordhelperapp/jvm/Main$Simple.id:I```这个按一定规则组织起来的字符串，就是一个符号引用。

**直接引用**

以```Simple```的id字段为例，直接引用就是虚拟机为id分配的内存地址。

**解析主要针对：**
1. 类或接口；
2. 字段；
3. 类方法；
4. 接口方法。

### 初始化

初始化阶段是执行类构造器```<clinit>()```方法的过程，```<clinit>```是由编译器自动收集类中的所有类变量的赋值动作和静态语句块(static{})中的语句合并产生的。
如下Java代码：
```java
public class Main {
    static int id = 123;
    static double value;

    static {
        value = 99.0;
    }

}
```
合并之后的静态语句块为：
```
  static {};
    descriptor: ()V
    flags: ACC_STATIC
    Code:
      stack=2, locals=0, args_size=0
         0: bipush        123
         2: putstatic     #2                  // Field id:I
         5: ldc2_w        #3                  // double 99.0d
         8: putstatic     #5                  // Field value:D
        11: return

```






