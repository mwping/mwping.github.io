## 组件化

### 模块分层

#### 1.toolkit

工具库，只基于Android原生Api。

#### 2.common

各个业务线的公共模块，依赖toolkit、com.android.support库、开源库等，并定义注解、定义InvocationHandler。

#### 3.业务module

能独立运行，也能作为module被壳项目依赖。

#### 4.壳工程

依赖各个业务module。


### 组件通信

两个业务module A、B，他们之间没有依赖关系，但是要能互相唤起对方的页面、调用对方的类方法，用注解+反射+动态代理来实现。

1.定义需要的服务

```java
public interface ComponentService {
    @TargetClass("com.github.mwping.login.LoginActivity")
    @RouterType(RouterTypeEnum.JUMP)
    int goLogin(Activity activity, Bundle extras);

    @TargetClass("com.github.mwping.login.util.Calculator")
    @RouterType(RouterTypeEnum.FUNCTION)
    int add(int a, int b);
}
```

2.定义实际的功能类或Activity

```java
public class Calculator {
    public static int add(int a, int b) {
        return a + b;
    }
}
```
```java
public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        TextView textView = findViewById(R.id.tv_content);
        Bundle extras = getIntent().getExtras();
        textView.append("Welcome to login:\n");
        textView.append("name:");
        if (extras != null) {
            textView.append(extras.getString("name"));
        }
        textView.append("\n");
        textView.append("id:");
        if (extras != null) {
            textView.append(extras.getInt("id") + "");
        }
    }
}
```

3.定义InvocationHandler

```java
public class RouterInvocationHandler implements InvocationHandler {

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        String methodName = method.getName();
        String targetClassName = null;
        Annotation targetClassAnnotation = method.getAnnotation(TargetClass.class);
        if (targetClassAnnotation != null) {
            targetClassName = ((TargetClass) targetClassAnnotation).value();
        }
        RouterTypeEnum routerTypeEnum = null;
        Annotation routerTypeAnnotation = method.getAnnotation(RouterType.class);
        if (routerTypeAnnotation != null) {
            routerTypeEnum = ((RouterType) routerTypeAnnotation).value();
        }
        if (routerTypeEnum == RouterTypeEnum.JUMP) {
            /**
             * args[0]: Activity
             * args[1]: Bundle or null
             */
            Activity activity = (Activity) args[0];
            Intent intent = new Intent();
            intent.putExtras(args.length > 1 ? (Bundle) args[1] : null);
            intent.setClassName(activity, targetClassName);
            try {
                activity.startActivity(intent);
            } catch (Exception e) {
                Toast.makeText(activity, e.getMessage(), Toast.LENGTH_SHORT).show();
            }
        } else if (routerTypeEnum == RouterTypeEnum.FUNCTION) {
            Class cls = getClass().getClassLoader().loadClass(targetClassName);
            Class<?>[] classList = new Class[args.length];
            for (int i = 0; i < classList.length; i++) {
                classList[i] = args[i].getClass();
                if (classList[i] == Integer.class) {
                    classList[i] = int.class;
                }
            }
            /**
             * 获取目标类同名、同参数的方法
             */
            Method targetMethod = cls.getDeclaredMethod(methodName, classList);
            if (targetMethod != null) {
                return targetMethod.invoke(cls.newInstance(), args);
            }
        }
        return 0;
    }
}

```

4.调用

```
public class MainActivity extends AppCompatActivity {
    ComponentService service;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        service = Router.getInstance().create(ComponentService.class);
    }

    public void goLogin(View view) {
        Bundle extras = new Bundle();
        extras.putString("name", "xiaoming");
        extras.putInt("id", 2018);
        service.goLogin(this, extras);
    }

    public void add(View view) {
        int a = 4;
        int b = 5;
        Toast.makeText(this, String.format("%1$s+%2$s=%3$s", a, b, service.add(a, b)),
                Toast.LENGTH_SHORT).show();
    }
}
```

### 总结

注解+动态代理+反射的方式，能做到：

1. 各个业务模块独立运行，互不依赖；
2. 新增或者删除某个业务模块，均不影响壳工程的正常编译；
3. 支持界面跳转、传递参数；
4. 支持普通方法调用、获取返回结果。








