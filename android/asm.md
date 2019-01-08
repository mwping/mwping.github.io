## ASM指南

### 目录

* ##### [关于ASM](#1)
  1. [官网地址](#1.1)

* ##### [打印Log示例](#2)
  1. [查看ASMifier文档](#2.1)
  2. [使用ASMifier](#2.2)
  3. [为方法生成字节码](#2.3)
  4. [自动调用系统Log](#2.4)

<h3 id="1">关于ASM</h3>

<h4 id="1.1">官网地址</h4> 
[https://asm.ow2.io/index.html](https://asm.ow2.io/index.html)

<h3 id="2">打印Log示例</h3>

<h4 id="2.1">查看ASMifier文档</h4>

文档连接：[https://asm.ow2.io/asm4-guide.pdf](https://asm.ow2.io/asm4-guide.pdf)，使用方法：
```
java -classpath asm.jar:asm-util.jar \
org.objectweb.asm.util.ASMifier \
java.lang.Runnable
```

<h4 id="2.2">使用ASMifier</h4>

1.依赖asm-all库：
```
compile 'org.ow2.asm:asm-all:6.0_BETA'
```

2.找到asm.jar，路径一般为：
```
/Users/lixiang/.gradle/caches/modules-2/files-2.1/org.ow2.asm/asm-all/6.0_BETA/535f141f6c8fc65986a3469839a852a3266d1025/asm-all-6.0_BETA.jar
```

3.编写一个测试类：
```java
public class AsmTest {
    @MwpLog
    public void testLog(int anInt, long aLong, boolean aBoolean, float aFloat,
                        double aDouble, String aString, LogObject object) {
    }
}
```
build项目，找到AsmTest.class:
> /Users/lixiang/Mwp/Github/TheMatrix/TheMatrixApp/app/build/intermediates/javac/debug/compileDebugJavaWithJavac/classes/com/github/mwping/lordhelperapp/util/AsmTest.class

4.使用ASMifier:
```
java -classpath /Users/lixiang/.gradle/caches/modules-2/files-2.1/org.ow2.asm/asm-all/6.0_BETA/535f141f6c8fc65986a3469839a852a3266d1025/asm-all-6.0_BETA.jar:asm-util.jar \
org.objectweb.asm.util.ASMifier \
/Users/lixiang/Mwp/Github/TheMatrix/TheMatrixApp/app/build/intermediates/javac/debug/compileDebugJavaWithJavac/classes/com/github/mwping/lordhelperapp/util/AsmTest.class
```
输出按java格式化：
```java
package asm.com.github.mwping.lordhelperapp.util;

import java.util.*;

import org.objectweb.asm.*;

public class AsmTestDump implements Opcodes {

    public static byte[] dump() throws Exception {

        ClassWriter cw = new ClassWriter(0);
        FieldVisitor fv;
        MethodVisitor mv;
        AnnotationVisitor av0;

        cw.visit(V1_7, ACC_PUBLIC + ACC_SUPER, "com/github/mwping/lordhelperapp/util/AsmTest", null, "java/lang/Object", null);

        {
            mv = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            mv.visitCode();
            mv.visitVarInsn(ALOAD, 0);
            mv.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            mv.visitInsn(RETURN);
            mv.visitMaxs(1, 1);
            mv.visitEnd();
        }
        {
            mv = cw.visitMethod(ACC_PUBLIC, "testLog", "(IJZFDLjava/lang/String;Lcom/github/mwping/lordhelperapp/util/LogObject;)V", null, null);
            {
                av0 = mv.visitAnnotation("Lcom/github/mwping/asm/annotation/MwpLog;", false);
                av0.visitEnd();
            }
            mv.visitCode();
            mv.visitInsn(RETURN);
            mv.visitMaxs(0, 10);
            mv.visitEnd();
        }
        cw.visitEnd();

        return cw.toByteArray();
    }
}
```

<h4 id="2.3">为方法生成字节码</h4>

修改类AsmTest.java:
```java
public class AsmTest {
    @MwpLog
    public void testLog(int anInt, long aLong, boolean aBoolean, float aFloat,
                        double aDouble, String aString, LogObject object) {
        StringBuilder builder = new StringBuilder();
        builder.append(anInt);
        builder.append(aLong);
        builder.append(aBoolean);
        builder.append(aFloat);
        builder.append(aDouble);
        builder.append(aString);
        builder.append(object);
    }
}
```
重新执行命令，获取格式化结果：
```java
package asm.com.github.mwping.lordhelperapp.util;

import java.util.*;

import org.objectweb.asm.*;

public class AsmTestDump implements Opcodes {

    public static byte[] dump() throws Exception {

        ClassWriter cw = new ClassWriter(0);
        FieldVisitor fv;
        MethodVisitor mv;
        AnnotationVisitor av0;

        cw.visit(V1_7, ACC_PUBLIC + ACC_SUPER, "com/github/mwping/lordhelperapp/util/AsmTest", null, "java/lang/Object", null);

        {
            mv = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            mv.visitCode();
            mv.visitVarInsn(ALOAD, 0);
            mv.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            mv.visitInsn(RETURN);
            mv.visitMaxs(1, 1);
            mv.visitEnd();
        }
        {
            mv = cw.visitMethod(ACC_PUBLIC, "testLog", "(IJZFDLjava/lang/String;Lcom/github/mwping/lordhelperapp/util/LogObject;)V", null, null);
            {
                av0 = mv.visitAnnotation("Lcom/github/mwping/asm/annotation/MwpLog;", false);
                av0.visitEnd();
            }
            mv.visitCode();
            mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
            mv.visitInsn(DUP);
            mv.visitMethodInsn(INVOKESPECIAL, "java/lang/StringBuilder", "<init>", "()V", false);
            mv.visitVarInsn(ASTORE, 10);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ILOAD, 1);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(I)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(LLOAD, 2);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(J)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ILOAD, 4);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Z)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(FLOAD, 5);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(F)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(DLOAD, 6);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(D)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ALOAD, 8);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ALOAD, 9);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/Object;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitInsn(RETURN);
            mv.visitMaxs(3, 11);
            mv.visitEnd();
        }
        cw.visitEnd();

        return cw.toByteArray();
    }
}
```

使用diff工具查看两次输出的区别：

![](../assets/images/asm-diff.png)

把AsmTest.java还原:
```java
public class AsmTest {
    @MwpLog
    public void testLog() {

    }
}
```

重写AdviceAdapter以下几个方法，其中onMethodExit内容均从上面的diff部分拷贝过来:
```java
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        if (desc.contains("MwpLog")) {
            enableLog = true;
        }
        return super.visitAnnotation(desc, visible);
    }

    @Override
    protected void onMethodEnter() {
        if (enableLog) {

        }
    }

    @Override
    protected void onMethodExit(int opcode) {
        if (enableLog) {
            mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
            mv.visitInsn(DUP);
            mv.visitMethodInsn(INVOKESPECIAL, "java/lang/StringBuilder", "<init>", "()V", false);
            mv.visitVarInsn(ASTORE, 10);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ILOAD, 1);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(I)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(LLOAD, 2);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(J)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ILOAD, 4);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Z)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(FLOAD, 5);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(F)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(DLOAD, 6);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(D)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ALOAD, 8);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
            mv.visitVarInsn(ALOAD, 10);
            mv.visitVarInsn(ALOAD, 9);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/Object;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);
        }
    }
```

build项目，重新查看AsmTest.class:
```java
public class AsmTest {
    public AsmTest() {
    }

    @MwpLog
    public void testLog(int anInt, long aLong, boolean aBoolean, float aFloat, double aDouble, String aString, LogObject object) {
        StringBuilder var10 = new StringBuilder();
        var10.append(anInt);
        var10.append(aLong);
        var10.append(aBoolean);
        var10.append(aFloat);
        var10.append(aDouble);
        var10.append(aString);
        var10.append(object);
    }
}
```

字节码生成成功！

<h4 id="2.4">自动调用系统Log</h4>
进一步重写方法：
```java
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        if (desc.contains("MwpLog")) {
            enableLog = true;
        }
        return super.visitAnnotation(desc, visible);
    }

    int startTimeId;

    @Override
    protected void onMethodEnter() {
        if (enableLog) {
            startTimeId = newLocal(Type.LONG_TYPE);
            mv.visitMethodInsn(INVOKESTATIC, "java/lang/System", "currentTimeMillis", "()J", false);
            mv.visitVarInsn(LSTORE, startTimeId);
        }
    }

    @Override
    protected void onMethodExit(int opcode) {
        if (enableLog) {
            int endTimeId = newLocal(Type.LONG_TYPE);
            mv.visitMethodInsn(INVOKESTATIC, "java/lang/System", "currentTimeMillis", "()J", false);
            mv.visitVarInsn(LSTORE, endTimeId);

            mv.visitVarInsn(LLOAD, endTimeId);
            mv.visitVarInsn(LLOAD, startTimeId);

            int costTimeId = newLocal(Type.LONG_TYPE);
            mv.visitInsn(LSUB);
            mv.visitVarInsn(LSTORE, costTimeId);

            int stringBuilderId = newLocal(Type.getType(StringBuilder.class));
            mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
            mv.visitInsn(DUP);
            mv.visitMethodInsn(INVOKESPECIAL, "java/lang/StringBuilder", "<init>", "()V", false);
            mv.visitVarInsn(ASTORE, stringBuilderId);

            mv.visitVarInsn(ALOAD, stringBuilderId);
            mv.visitLdcInsn(" \n┌─────────────────────────────────────────────────\n│" + methodName);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);

            if (args != null && args.length > 0) {
                int index = 1;

                mv.visitVarInsn(ALOAD, stringBuilderId);
                mv.visitLdcInsn("\n│args:");
                mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
                mv.visitInsn(POP);

                for (Type arg : args) {

                    mv.visitVarInsn(ALOAD, stringBuilderId);
                    mv.visitLdcInsn("\n│\t");
                    mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
                    mv.visitInsn(POP);

                    mv.visitVarInsn(ALOAD, stringBuilderId);
                    switch (arg.getSort()) {
                        case Type.INT: {
                            mv.visitVarInsn(ILOAD, index);
                            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(I)Ljava/lang/StringBuilder;", false);
                            index++;
                            break;
                        }
                        case Type.BOOLEAN: {
                            mv.visitVarInsn(ILOAD, index);
                            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Z)Ljava/lang/StringBuilder;", false);
                            index++;
                            break;
                        }
                        case Type.LONG: {
                            mv.visitVarInsn(LLOAD, index);
                            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(J)Ljava/lang/StringBuilder;", false);
                            index += 2;
                            break;
                        }
                        case Type.FLOAT: {
                            mv.visitVarInsn(FLOAD, index);
                            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(F)Ljava/lang/StringBuilder;", false);
                            index++;
                            break;
                        }
                        case Type.DOUBLE: {
                            mv.visitVarInsn(DLOAD, index);
                            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(D)Ljava/lang/StringBuilder;", false);
                            index += 2;
                            break;
                        }
                        case Type.OBJECT: {
                            mv.visitVarInsn(ALOAD, index);
                            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/Object;)Ljava/lang/StringBuilder;", false);
                            index++;
                            break;
                        }
                        default: {
                            index++;
                            break;
                        }
                    }
                    mv.visitInsn(POP);
                }
            }


            mv.visitVarInsn(ALOAD, stringBuilderId);
            mv.visitLdcInsn("\n│cost time:");
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);

            mv.visitVarInsn(ALOAD, stringBuilderId);
            mv.visitVarInsn(LLOAD, costTimeId);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(J)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);

            mv.visitVarInsn(ALOAD, stringBuilderId);
            mv.visitLdcInsn("ms");
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);

            mv.visitVarInsn(ALOAD, stringBuilderId);
            mv.visitLdcInsn("\n└─────────────────────────────────────────────────");
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
            mv.visitInsn(POP);

            mv.visitLdcInsn("MwpLog::" + className.substring(className.lastIndexOf("/") + 1));
            mv.visitVarInsn(ALOAD, stringBuilderId);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;", false);
            mv.visitMethodInsn(INVOKESTATIC, "android/util/Log", "d", "(Ljava/lang/String;Ljava/lang/String;)I", false);
            mv.visitInsn(POP);
        }
    }
```
测试log代码：
```java
        AsmTest asmTest = new AsmTest();
        asmTest.testLog(2019,
                System.currentTimeMillis(),
                true,
                1f / 3,
                Math.PI,
                "hello",
                new LogObject(100, "ASM")
        );
```
```java

public class AsmTest {
    @MwpLog
    public void testLog(int anInt, long aLong, boolean aBoolean, float aFloat,
                        double aDouble, String aString, LogObject object) {
        try {
            Thread.sleep(1230);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```
```java
public class LogObject {
    private int index;
    private String name;

    public LogObject(int index, String name) {
        this.index = index;
        this.name = name;
    }

    @Override
    public String toString() {
        return "LogObject{" +
                "index=" + index +
                ", name='" + name + '\'' +
                '}';
    }
}
```
查看输出：
```
2019-01-08 23:51:17.223 8853-8853/com.github.mwping.lordhelperapp D/MwpLog::AsmTest:  
    ┌─────────────────────────────────────────────────
    │testLog
    │args:
    │   2019
    │   1546962675993
    │   true
    │   0.33333334
    │   3.141592653589793
    │   hello
    │   LogObject{index=100, name='ASM'}
    │cost time:1230ms
    └─────────────────────────────────────────────────
```