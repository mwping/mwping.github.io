## 单例模式

* ##### [应用场景](#1)
  1. [EventBus](#1.1)

<h3 id="1">应用场景</h3>

<img src="../assets/images/edraw/singleton_useage.png" width="390">

<h4 id="1.1">EventBus</h4> 

```java
public class EventBus {

    static volatile EventBus defaultInstance;
    
    /** Convenience singleton for apps using a process-wide EventBus instance. */
    public static EventBus getDefault() {
        EventBus instance = defaultInstance;
        if (instance == null) {
            synchronized (EventBus.class) {
                instance = EventBus.defaultInstance;
                if (instance == null) {
                    instance = EventBus.defaultInstance = new EventBus();
                }
            }
        }
        return instance;
    }
}
```