## 泛型中的super和extends

```java
    static class Plate<T> {
        T item;

        public Plate(T item) {
            this.item = item;
        }

        public T getItem() {
            return item;
        }

        public void setItem(T item) {
            this.item = item;
        }
    }

    static class Fruit {

    }

    static class Apple extends Fruit {

    }

    static class Banana extends Fruit {

    }
```

测试代码：
```java
        Plate<? extends Fruit> plate = new Plate<>(new Apple());

//        plate.setItem(new Fruit());// error
//        plate.setItem(new Apple());// error
//        plate.setItem(new Banana());// error

        Fruit fruit = plate.getItem();
//        Apple apple = plate.getItem();// error
//        Banana banana = plate.getItem();// error
```

```java
        Plate<? super Fruit> plate = new Plate<>(new Fruit());

        plate.setItem(new Fruit());
        plate.setItem(new Apple());
        plate.setItem(new Banana());
//        plate.setItem(new Object());// error

        Object object = plate.getItem();
//        Fruit fruit = plate.getItem();// error
//        Apple apple = plate.getItem();// error
//        Banana banana = plate.getItem();// error
```