## 插件化

```java
public class MyApplication extends Application {
    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
        try {
            HookHelper.hookInstrumentation(base);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

```java
public class HookHelper {
    public static final String TARGET_INTENT = "target_intent";

    public static void hookInstrumentation(Context context) throws Exception {
        Class<?> contextImplClass = Class.forName("android.app.ContextImpl");
        Field mMainThreadField = FieldUtil.getField(contextImplClass, "mMainThread");
        Object activityThread = mMainThreadField.get(context);
        Class<?> activityThreadClass = Class.forName("android.app.ActivityThread");
        Field mInstrumentationField = FieldUtil.getField(activityThreadClass, "mInstrumentation");
        FieldUtil.setField(activityThreadClass, activityThread, "mInstrumentation",
                new InstrumentationProxy((Instrumentation) mInstrumentationField.get(activityThread),
                        context.getPackageManager()));
    }
}
```

```java
public class InstrumentationProxy extends Instrumentation {
    private Instrumentation mInstrumentation;
    private PackageManager mPackageManager;

    public InstrumentationProxy(Instrumentation instrumentation, PackageManager packageManager) {
        mInstrumentation = instrumentation;
        mPackageManager = packageManager;
    }

    public ActivityResult execStartActivity(
            Context who, IBinder contextThread, IBinder token, Activity target,
            Intent intent, int requestCode, Bundle options) {
        List<ResolveInfo> infos = mPackageManager.queryIntentActivities(intent, PackageManager.MATCH_ALL);
        if (infos == null || infos.size() == 0) {
            intent.putExtra(HookHelper.TARGET_INTENT, intent.getComponent().getClassName());
            intent.setClassName(who, StubActivity.class.getName());
        }
        try {
            Method execMethod = Instrumentation.class.getDeclaredMethod("execStartActivity",
                    Context.class, IBinder.class, IBinder.class, Activity.class, Intent.class, int.class, Bundle.class);
            return (ActivityResult) execMethod.invoke(mInstrumentation, who, contextThread, token,
                    target, intent, requestCode, options);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public Activity newActivity(ClassLoader cl, String className, Intent intent) throws InstantiationException,
            IllegalAccessException, ClassNotFoundException {
        String intentName = intent.getStringExtra(HookHelper.TARGET_INTENT);
        if (!TextUtils.isEmpty(intentName)) {
            return super.newActivity(cl, intentName, intent);
        }
        return super.newActivity(cl, className, intent);
    }
}
```
下载插件apk之后，把插件apk路径下面的dexElements合并到系统的类加载器中：
```java
    DexClassLoader loader = new DexClassLoader(
            file.getAbsolutePath(),//apk文件路径
            getDir("dex", Context.MODE_PRIVATE).getAbsolutePath(),
            null,//不涉及.so文件的话，传null即可
            getClassLoader());//双亲委派
    DexUtil.insertDex(loader, getClassLoader());
```
```java
public class DexUtil {
    public static void insertDex(DexClassLoader dexClassLoader, ClassLoader baseClassLoader) throws Exception {
        Object baseDexElements = getDexElements(getPathList(baseClassLoader));
        Object newDexElements = getDexElements(getPathList(dexClassLoader));
        Object allDexElements = combineArray(baseDexElements, newDexElements);
        Object pathList = getPathList(baseClassLoader);
        Reflector.with(pathList).field("dexElements").set(allDexElements);
    }

    private static Object getDexElements(Object pathList) throws Exception {
        return Reflector.with(pathList).field("dexElements").get();
    }

    private static Object getPathList(ClassLoader baseDexClassLoader) throws Exception {
        return Reflector.with(baseDexClassLoader).field("pathList").get();
    }

    private static Object combineArray(Object firstArray, Object secondArray) {
        Class<?> localClass = firstArray.getClass().getComponentType();
        int firstArrayLength = Array.getLength(firstArray);
        int secondArrayLength = Array.getLength(secondArray);
        Object result = Array.newInstance(localClass, firstArrayLength + secondArrayLength);
        System.arraycopy(firstArray, 0, result, 0, firstArrayLength);
        System.arraycopy(secondArray, 0, result, firstArrayLength, secondArrayLength);
        return result;
    }
}
```

合并前：

![](../assets/images/base_classloader_dexelements.png?v=1)
![](../assets/images/my_classloader_dexelements.png?v=1)

合并后，系统的类加载器新增了自定义的apk路径，这样它就能加载两个目录下面的类文件了。

![](../assets/images/combine_classloader_dexelements.png?v=1)

启动插件apk里面的Activity：
```java
    Intent intent = new Intent();
    intent.setClassName(this, "com.github.mwping.pluggableclientapp.MainActivity");
    startActivity(intent);
```