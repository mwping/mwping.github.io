## adb shell am 命令和ActivityManagerService

### am脚本

adb shell am命令会执行am脚本：

/Volumes/Android/aosp/frameworks/base/cmds/am/am
```
#!/system/bin/sh

if [ "$1" != "instrument" ] ; then
    cmd activity "$@"
else
    base=/system
    export CLASSPATH=$base/framework/am.jar
    exec app_process $base/bin com.android.commands.am.Am "$@"
fi
```

脚本会调用/Volumes/Android/aosp/frameworks/base/cmds/am/src/com/android/commands/am/Am.java的main方法：
```java
public class Am extends BaseCommand {
    /**
     * Command-line entry point.
     *
     * @param args The command-line arguments
     */
    public static void main(String[] args) {
        (new Am()).run(args);
    }

    @Override
    public void onRun() throws Exception {

        mAm = ActivityManager.getService();
        if (mAm == null) {
            System.err.println(NO_SYSTEM_ERROR_CODE);
            throw new AndroidException("Can't connect to activity manager; is the system running?");
        }

        mPm = IPackageManager.Stub.asInterface(ServiceManager.getService("package"));
        if (mPm == null) {
            System.err.println(NO_SYSTEM_ERROR_CODE);
            throw new AndroidException("Can't connect to package manager; is the system running?");
        }

        String op = nextArgRequired();

        if (op.equals("instrument")) {
            runInstrument();
        } else {
        	// go here
            runAmCmd(getRawArgs());
        }
    }

    void runAmCmd(String[] args) throws AndroidException {
        final MyShellCallback cb = new MyShellCallback();
        try {
      		// AIDL跨进程调用ActivityManagerService的shellCommand方法(父类Binder的方法)
            mAm.asBinder().shellCommand(FileDescriptor.in, FileDescriptor.out, FileDescriptor.err,
                    args, cb, new ResultReceiver(null) { });
        } catch (RemoteException e) {
            System.err.println(NO_SYSTEM_ERROR_CODE);
            throw new AndroidException("Can't call activity manager; is the system running?");
        } finally {
            cb.mActive = false;
        }
    }
}
```

shellCommand方法跨进程调用ActivityManagerService的shellCommand方法(父类Binder的方法)，ActivityManagerService重写onShellCommand响应命令：

```java
public class ActivityManagerService extends IActivityManager.Stub
        implements Watchdog.Monitor, BatteryStatsImpl.BatteryCallback {

    @Override
    public void onShellCommand(FileDescriptor in, FileDescriptor out,
            FileDescriptor err, String[] args, ShellCallback callback,
            ResultReceiver resultReceiver) {
        (new ActivityManagerShellCommand(this, false)).exec(
                this, in, out, err, args, callback, resultReceiver);
    }
}
```
ActivityManagerShellCommand的onCommand方法处理各种命令：

```java
final class ActivityManagerShellCommand extends ShellCommand {

    @Override
    public int onCommand(String cmd) {
        if (cmd == null) {
            return handleDefaultCommands(cmd);
        }
        PrintWriter pw = getOutPrintWriter();
        try {
            switch (cmd) {
                case "start":
                case "start-activity":
                    return runStartActivity(pw);
                case "startservice":
                case "start-service":
                    return runStartService(pw, false);
                case "startforegroundservice":
                case "startfgservice":
                case "start-foreground-service":
                case "start-fg-service":
                    return runStartService(pw, true);
                case "stopservice":
                case "stop-service":
                    return runStopService(pw);
                case "broadcast":
                    return runSendBroadcast(pw);
                case "instrument":
                    getOutPrintWriter().println("Error: must be invoked through 'am instrument'.");
                    return -1;
                case "trace-ipc":
                    return runTraceIpc(pw);
                case "profile":
                    return runProfile(pw);
                case "dumpheap":
                    return runDumpHeap(pw);
                case "set-debug-app":
                    return runSetDebugApp(pw);
                case "clear-debug-app":
                    return runClearDebugApp(pw);
                case "set-watch-heap":
                    return runSetWatchHeap(pw);
                case "clear-watch-heap":
                    return runClearWatchHeap(pw);
                case "bug-report":
                    return runBugReport(pw);
                case "force-stop":
                    return runForceStop(pw);
                case "crash":
                    return runCrash(pw);
                case "kill":
                    return runKill(pw);
                case "kill-all":
                    return runKillAll(pw);
                case "make-uid-idle":
                    return runMakeIdle(pw);
                case "monitor":
                    return runMonitor(pw);
                case "watch-uids":
                    return runWatchUids(pw);
                case "hang":
                    return runHang(pw);
                case "restart":
                    return runRestart(pw);
                case "idle-maintenance":
                    return runIdleMaintenance(pw);
                case "screen-compat":
                    return runScreenCompat(pw);
                case "package-importance":
                    return runPackageImportance(pw);
                case "to-uri":
                    return runToUri(pw, 0);
                case "to-intent-uri":
                    return runToUri(pw, Intent.URI_INTENT_SCHEME);
                case "to-app-uri":
                    return runToUri(pw, Intent.URI_ANDROID_APP_SCHEME);
                case "switch-user":
                    return runSwitchUser(pw);
                case "get-current-user":
                    return runGetCurrentUser(pw);
                case "start-user":
                    return runStartUser(pw);
                case "unlock-user":
                    return runUnlockUser(pw);
                case "stop-user":
                    return runStopUser(pw);
                case "is-user-stopped":
                    return runIsUserStopped(pw);
                case "get-started-user-state":
                    return runGetStartedUserState(pw);
                case "track-associations":
                    return runTrackAssociations(pw);
                case "untrack-associations":
                    return runUntrackAssociations(pw);
                case "get-uid-state":
                    return getUidState(pw);
                case "get-config":
                    return runGetConfig(pw);
                case "suppress-resize-config-changes":
                    return runSuppressResizeConfigChanges(pw);
                case "set-inactive":
                    return runSetInactive(pw);
                case "get-inactive":
                    return runGetInactive(pw);
                case "send-trim-memory":
                    return runSendTrimMemory(pw);
                case "display":
                    return runDisplay(pw);
                case "stack":
                    return runStack(pw);
                case "task":
                    return runTask(pw);
                case "write":
                    return runWrite(pw);
                case "attach-agent":
                    return runAttachAgent(pw);
                case "supports-multiwindow":
                    return runSupportsMultiwindow(pw);
                case "supports-split-screen-multi-window":
                    return runSupportsSplitScreenMultiwindow(pw);
                case "update-appinfo":
                    return runUpdateApplicationInfo(pw);
                case "no-home-screen":
                    return runNoHomeScreen(pw);
                case "wait-for-broadcast-idle":
                    return runWaitForBroadcastIdle(pw);
                default:
                    return handleDefaultCommands(cmd);
            }
        } catch (RemoteException e) {
            pw.println("Remote exception: " + e);
        }
        return -1;
    }
}
```

假设命令行执行下面的命令，通过指定包名、Activity类名来启动Activity：
```
$ adb shell am start -n com.example.app/.ExampleActivity
```
会调用ActivityManagerShellCommand的runStartActivity方法：
```java
final class ActivityManagerShellCommand extends ShellCommand {

	int runStartActivity(PrintWriter pw) throws RemoteException {
        Intent intent;
        try {
            intent = makeIntent(UserHandle.USER_CURRENT);
        } catch (URISyntaxException e) {
            throw new RuntimeException(e.getMessage(), e);
        }

        if (mUserId == UserHandle.USER_ALL) {
            getErrPrintWriter().println("Error: Can't start service with user 'all'");
            return 1;
        }

        String mimeType = intent.getType();
        if (mimeType == null && intent.getData() != null
                && "content".equals(intent.getData().getScheme())) {
            mimeType = mInterface.getProviderMimeType(intent.getData(), mUserId);
        }

        do {
            if (mStopOption) {
                String packageName;
                if (intent.getComponent() != null) {
                    packageName = intent.getComponent().getPackageName();
                } else {
                    List<ResolveInfo> activities = mPm.queryIntentActivities(intent, mimeType, 0,
                            mUserId).getList();
                    if (activities == null || activities.size() <= 0) {
                        getErrPrintWriter().println("Error: Intent does not match any activities: "
                                + intent);
                        return 1;
                    } else if (activities.size() > 1) {
                        getErrPrintWriter().println(
                                "Error: Intent matches multiple activities; can't stop: "
                                + intent);
                        return 1;
                    }
                    packageName = activities.get(0).activityInfo.packageName;
                }
                pw.println("Stopping: " + packageName);
                pw.flush();
                mInterface.forceStopPackage(packageName, mUserId);
                try {
                    Thread.sleep(250);
                } catch (InterruptedException e) {
                }
            }

            ProfilerInfo profilerInfo = null;

            if (mProfileFile != null || mAgent != null) {
                ParcelFileDescriptor fd = null;
                if (mProfileFile != null) {
                    fd = openOutputFileForSystem(mProfileFile);
                    if (fd == null) {
                        return 1;
                    }
                }
                profilerInfo = new ProfilerInfo(mProfileFile, fd, mSamplingInterval, mAutoStop,
                        mStreaming, mAgent);
            }

            pw.println("Starting: " + intent);
            pw.flush();
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

            WaitResult result = null;
            int res;
            final long startTime = SystemClock.uptimeMillis();
            ActivityOptions options = null;
            if (mDisplayId != INVALID_DISPLAY) {
                options = ActivityOptions.makeBasic();
                options.setLaunchDisplayId(mDisplayId);
            }
            if (mStackId != INVALID_STACK_ID) {
                options = ActivityOptions.makeBasic();
                options.setLaunchStackId(mStackId);
            }
            if (mTaskId != INVALID_TASK_ID) {
                options = ActivityOptions.makeBasic();
                options.setLaunchTaskId(mTaskId);

                if (mIsTaskOverlay) {
                    options.setTaskOverlay(true, true /* canResume */);
                }
            }
            if (mWaitOption) {
                result = mInterface.startActivityAndWait(null, null, intent, mimeType,
                        null, null, 0, mStartFlags, profilerInfo,
                        options != null ? options.toBundle() : null, mUserId);
                res = result.result;
            } else {
                res = mInterface.startActivityAsUser(null, null, intent, mimeType,
                        null, null, 0, mStartFlags, profilerInfo,
                        options != null ? options.toBundle() : null, mUserId);
            }
            final long endTime = SystemClock.uptimeMillis();
            PrintWriter out = mWaitOption ? pw : getErrPrintWriter();
            boolean launched = false;
            switch (res) {
                case ActivityManager.START_SUCCESS:
                    launched = true;
                    break;
                case ActivityManager.START_SWITCHES_CANCELED:
                    launched = true;
                    out.println(
                            "Warning: Activity not started because the "
                                    + " current activity is being kept for the user.");
                    break;
                case ActivityManager.START_DELIVERED_TO_TOP:
                    launched = true;
                    out.println(
                            "Warning: Activity not started, intent has "
                                    + "been delivered to currently running "
                                    + "top-most instance.");
                    break;
                case ActivityManager.START_RETURN_INTENT_TO_CALLER:
                    launched = true;
                    out.println(
                            "Warning: Activity not started because intent "
                                    + "should be handled by the caller");
                    break;
                case ActivityManager.START_TASK_TO_FRONT:
                    launched = true;
                    out.println(
                            "Warning: Activity not started, its current "
                                    + "task has been brought to the front");
                    break;
                case ActivityManager.START_INTENT_NOT_RESOLVED:
                    out.println(
                            "Error: Activity not started, unable to "
                                    + "resolve " + intent.toString());
                    break;
                case ActivityManager.START_CLASS_NOT_FOUND:
                    out.println(NO_CLASS_ERROR_CODE);
                    out.println("Error: Activity class " +
                            intent.getComponent().toShortString()
                            + " does not exist.");
                    break;
                case ActivityManager.START_FORWARD_AND_REQUEST_CONFLICT:
                    out.println(
                            "Error: Activity not started, you requested to "
                                    + "both forward and receive its result");
                    break;
                case ActivityManager.START_PERMISSION_DENIED:
                    out.println(
                            "Error: Activity not started, you do not "
                                    + "have permission to access it.");
                    break;
                case ActivityManager.START_NOT_VOICE_COMPATIBLE:
                    out.println(
                            "Error: Activity not started, voice control not allowed for: "
                                    + intent);
                    break;
                case ActivityManager.START_NOT_CURRENT_USER_ACTIVITY:
                    out.println(
                            "Error: Not allowed to start background user activity"
                                    + " that shouldn't be displayed for all users.");
                    break;
                default:
                    out.println(
                            "Error: Activity not started, unknown error code " + res);
                    break;
            }
            out.flush();
            if (mWaitOption && launched) {
                if (result == null) {
                    result = new WaitResult();
                    result.who = intent.getComponent();
                }
                pw.println("Status: " + (result.timeout ? "timeout" : "ok"));
                if (result.who != null) {
                    pw.println("Activity: " + result.who.flattenToShortString());
                }
                if (result.thisTime >= 0) {
                    pw.println("ThisTime: " + result.thisTime);
                }
                if (result.totalTime >= 0) {
                    pw.println("TotalTime: " + result.totalTime);
                }
                pw.println("WaitTime: " + (endTime-startTime));
                pw.println("Complete");
                pw.flush();
            }
            mRepeat--;
            if (mRepeat > 0) {
                mInterface.unhandledBack();
            }
        } while (mRepeat > 0);
        return 0;
    }

    private Intent makeIntent(int defUser) throws URISyntaxException {
        mStartFlags = 0;
        mWaitOption = false;
        mStopOption = false;
        mRepeat = 0;
        mProfileFile = null;
        mSamplingInterval = 0;
        mAutoStop = false;
        mStreaming = false;
        mUserId = defUser;
        mDisplayId = INVALID_DISPLAY;
        mStackId = INVALID_STACK_ID;
        mTaskId = INVALID_TASK_ID;
        mIsTaskOverlay = false;

        return Intent.parseCommandArgs(this, new Intent.CommandOptionHandler() {
            @Override
            public boolean handleOption(String opt, ShellCommand cmd) {
                // ... 省略部分代码
                return true;
            }
        });
    }
}
```
Intent.parseCommandArgs方法处理-n参数：
```java
public class Intent implements Parcelable, Cloneable {
    public static Intent parseCommandArgs(ShellCommand cmd, CommandOptionHandler optionHandler)
            throws URISyntaxException {
        Intent intent = new Intent();
        Intent baseIntent = intent;
        boolean hasIntentInfo = false;

        Uri data = null;
        String type = null;

        String opt;
        while ((opt=cmd.getNextOption()) != null) {
            switch (opt) {
                case "-n": {
                    String str = cmd.getNextArgRequired();
                    ComponentName cn = ComponentName.unflattenFromString(str);
                    if (cn == null)
                        throw new IllegalArgumentException("Bad component name: " + str);
                    intent.setComponent(cn);
                    if (intent == baseIntent) {
                        hasIntentInfo = true;
                    }
                }
                break;
                default:
                    if (optionHandler != null && optionHandler.handleOption(opt, cmd)) {
                        // Okay, caller handled this option.
                    } else {
                        throw new IllegalArgumentException("Unknown option: " + opt);
                    }
                    break;
            }
        }
        intent.setDataAndType(data, type);

        final boolean hasSelector = intent != baseIntent;
        if (hasSelector) {
            // A selector was specified; fix up.
            baseIntent.setSelector(intent);
            intent = baseIntent;
        }

        String arg = cmd.getNextArg();
        baseIntent = null;
        if (arg == null) {
            if (hasSelector) {
                // If a selector has been specified, and no arguments
                // have been supplied for the main Intent, then we can
                // assume it is ACTION_MAIN CATEGORY_LAUNCHER; we don't
                // need to have a component name specified yet, the
                // selector will take care of that.
                baseIntent = new Intent(Intent.ACTION_MAIN);
                baseIntent.addCategory(Intent.CATEGORY_LAUNCHER);
            }
        } else if (arg.indexOf(':') >= 0) {
            // The argument is a URI.  Fully parse it, and use that result
            // to fill in any data not specified so far.
            baseIntent = Intent.parseUri(arg, Intent.URI_INTENT_SCHEME
                    | Intent.URI_ANDROID_APP_SCHEME | Intent.URI_ALLOW_UNSAFE);
        } else if (arg.indexOf('/') >= 0) {
            // The argument is a component name.  Build an Intent to launch
            // it.
            baseIntent = new Intent(Intent.ACTION_MAIN);
            baseIntent.addCategory(Intent.CATEGORY_LAUNCHER);
            baseIntent.setComponent(ComponentName.unflattenFromString(arg));
        } else {
            // Assume the argument is a package name.
            baseIntent = new Intent(Intent.ACTION_MAIN);
            baseIntent.addCategory(Intent.CATEGORY_LAUNCHER);
            baseIntent.setPackage(arg);
        }
        if (baseIntent != null) {
            Bundle extras = intent.getExtras();
            intent.replaceExtras((Bundle)null);
            Bundle uriExtras = baseIntent.getExtras();
            baseIntent.replaceExtras((Bundle)null);
            if (intent.getAction() != null && baseIntent.getCategories() != null) {
                HashSet<String> cats = new HashSet<String>(baseIntent.getCategories());
                for (String c : cats) {
                    baseIntent.removeCategory(c);
                }
            }
            intent.fillIn(baseIntent, Intent.FILL_IN_COMPONENT | Intent.FILL_IN_SELECTOR);
            if (extras == null) {
                extras = uriExtras;
            } else if (uriExtras != null) {
                uriExtras.putAll(extras);
                extras = uriExtras;
            }
            intent.replaceExtras(extras);
            hasIntentInfo = true;
        }

        if (!hasIntentInfo) throw new IllegalArgumentException("No intent supplied");
        return intent;
    }
}
```
ComponentName.unflattenFromString分解字符串\"com.example.app/.ExampleActivity\"，得到ComponentName:

1. pkg=\"com.example.app\" 
2. cls=\"com.example.app.ExampleActivity\"：

```java
    /**
     * Recover a ComponentName from a String that was previously created with
     * {@link #flattenToString()}.  It splits the string at the first '/',
     * taking the part before as the package name and the part after as the
     * class name.  As a special convenience (to use, for example, when
     * parsing component names on the command line), if the '/' is immediately
     * followed by a '.' then the final class name will be the concatenation
     * of the package name with the string following the '/'.  Thus
     * "com.foo/.Blah" becomes package="com.foo" class="com.foo.Blah".
     *
     * @param str The String that was returned by flattenToString().
     * @return Returns a new ComponentName containing the package and class
     * names that were encoded in <var>str</var>
     *
     * @see #flattenToString()
     */
    public static @Nullable ComponentName unflattenFromString(@NonNull String str) {
        int sep = str.indexOf('/');
        if (sep < 0 || (sep+1) >= str.length()) {
            return null;
        }
        String pkg = str.substring(0, sep);
        String cls = str.substring(sep+1);
        if (cls.length() > 0 && cls.charAt(0) == '.') {
            cls = pkg + cls;
        }
        return new ComponentName(pkg, cls);
    }
```
创建完Intent之后，调用ActivityManagerService的startActivityAsUser方法：
```java
public class ActivityManagerService extends IActivityManager.Stub
        implements Watchdog.Monitor, BatteryStatsImpl.BatteryCallback {

    @Override
    public final int startActivityAsUser(IApplicationThread caller, String callingPackage,
            Intent intent, String resolvedType, IBinder resultTo, String resultWho, int requestCode,
            int startFlags, ProfilerInfo profilerInfo, Bundle bOptions, int userId) {
        enforceNotIsolatedCaller("startActivity");
        userId = mUserController.handleIncomingUser(Binder.getCallingPid(), Binder.getCallingUid(),
                userId, false, ALLOW_FULL_ONLY, "startActivity", null);
        // TODO: Switch to user app stacks here.
        return mActivityStarter.startActivityMayWait(caller, -1, callingPackage, intent,
                resolvedType, null, null, resultTo, resultWho, requestCode, startFlags,
                profilerInfo, null, null, bOptions, false, userId, null, "startActivityAsUser");
    }
}
```
后续就进入了Activity启动流程。运行示例：
```java
$ adb shell am start -n com.github.mwping.lordhelperapp/.activity.MainActivity
Starting: Intent { cmp=com.github.mwping.lordhelperapp/.activity.MainActivity }
```