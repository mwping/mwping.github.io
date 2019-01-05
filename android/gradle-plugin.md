## Gradle插件开发与发布指南

### 目录

* ##### [项目配置](#1)
  1. [创建Module](#1.1)
  2. [配置项目](#1.2)
  3. [调试插件](#1.3)

<h3 id="1">项目配置</h3>

<h4 id="1.1">创建Module</h4>

1. module名必须为buildSrc
2. 新建目录：buildSrc/src/main/groovy
3. 新建目录：buildSrc/src/main/resources/META-INF/gradle-plugins

<h4 id="1.2">配置项目</h4>

groovy目录下新建包名，如com.github.mwping.plugin，包下新建插件主类：MwpPlugin.groovy：
```java
package com.github.mwping.plugin

import com.github.mwping.plugin.utils.MwpLogger
import org.gradle.api.Plugin
import org.gradle.api.Project


class MwpPlugin implements Plugin<Project> {

    @Override
    void apply(Project project) {
        MwpLogger logger = new MwpLogger(project)
        logger.error("apply MwpPlugin")
    }
}
```
为了方便打印信息，增加MwpLogger.java：
```java
package com.github.mwping.plugin.utils;

import org.gradle.api.Project;
import org.gradle.api.logging.Logger;

public class MwpLogger {
    private static final char TOP_LEFT_CORNER = '┌';
    private static final char BOTTOM_LEFT_CORNER = '└';
    private static final char HORIZONTAL_LINE = '│';
    private static final String DIVIDER = "─────────────────────────────────────────────────";
    private Project project;
    private Logger logger;

    public MwpLogger(Project project) {
        this.project = project;
        logger = project.getLogger();
    }

    public void error(String s) {
        String info = String.format("%1$s\n%2$s %3$s\n%4$s", TOP_LEFT_CORNER + DIVIDER, HORIZONTAL_LINE, s, BOTTOM_LEFT_CORNER + DIVIDER);
        logger.error(info);
    }
}
```

gradle-plugins目录下新建文件com.github.mwping.plugin.properties：
```
implementation-class=com.github.mwping.plugin.MwpPlugin
```

修改buildSrc/build.gradle文件：
```
apply plugin: 'groovy'

dependencies {
    compile gradleApi() //gradle sdk
    compile localGroovy() //groovy sdk
}

repositories {
    jcenter()
}
```
项目整体目录如下：
![](../assets/images/gradle_plugin_module.png)

<h4 id="1.3">调试插件</h4>
在当前项目的application类型的module(如app)的build.gradle文件添加：
```
apply plugin: 'com.android.application'
apply plugin: com.github.mwping.plugin.MwpPlugin // add this line
```

命令行输入./gradlew clean -p app查看日志：
```
$ ./gradlew clean -p app

> Configure project :app 
┌─────────────────────────────────────────────────
│ apply MwpPlugin
└─────────────────────────────────────────────────


BUILD SUCCESSFUL in 1s
1 actionable task: 1 up-to-date
```
