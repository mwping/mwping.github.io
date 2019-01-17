
## 图解View绘制原理(软件渲染篇)

### 目录

* ##### [确认脏区域](#1)

* ##### [发起重绘](#2)

* ##### [重绘View树](#3)

<h3 id="1">确认脏区域</h3>

* 根据invalidate本身的View的mLeft、mRight、mBottom、mTop得到初始脏区域：Rect(0, 0 - 300, 300)；

* 父布局根据该View的mLeft=50、mTop=50，将脏区域矩形偏移，变为：Rect(50, 50 - 350, 350)；

* 祖父布局根据父布局的mLeft=50、mTop=300，将脏区域矩形偏移，变为：Rect(100, 350 - 400, 650)；

* 依次类推，直到布局的顶级根节点DecorView，偏移状态栏的高度(此处为126)，变为：Rect(100, 476 - 400, 776)。

![](../assets/images/invalidate_area.png)

最终确认脏区域在屏幕上的脏区域为Rect(100, 476 - 400, 776)，如下图：

![](../assets/images/invalidate_area2.png)

<h3 id="2">发起重绘</h3>

确认脏区域完毕，由ViewRootImpl发起重绘：

```java
    @Override
    public ViewParent invalidateChildInParent(int[] location, Rect dirty) {
    	// ...
        invalidateRectOnScreen(dirty);
        // ...
        return null;
    }

    private void invalidateRectOnScreen(Rect dirty) {
    	// ...
        scheduleTraversals();
        // ...
    }

    void doTraversal() {
    	// ...
        performTraversals();
        // ...
    }

    private void performTraversals() {
    	// ...
        performDraw();
        // ...
    }
    private boolean draw(boolean fullRedrawNeeded) {
    	// ...
    	drawSoftware(surface, mAttachInfo, xOffset, yOffset,
                        scalingRequired, dirty, surfaceInsets);
    	// ...
    }
    /**
     * @return true if drawing was successful, false if an error occurred
     */
    private boolean drawSoftware(Surface surface, AttachInfo attachInfo, int xoff, int yoff,
            boolean scalingRequired, Rect dirty, Rect surfaceInsets) {
        // Draw with software renderer.
        final Canvas canvas = surface.lockCanvas(dirty);
        // DecorView
        mView.draw(canvas);
        surface.unlockCanvasAndPost(canvas);
    }
```

<h3 id="3">重绘View树</h3>

由DecorView而下，重绘整个View树。

**注意：会排除与脏区域不相交的View，代码逻辑如下：**

View.java:
```java
    boolean draw(Canvas canvas, ViewGroup parent, long drawingTime) {
        if (canvas.quickReject(mLeft, mTop, mRight, mBottom, Canvas.EdgeType.BW)) {
            return ;
        }
    }
```

Canvas.java:
```java
    /**
     * Return true if the specified rectangle, after being transformed by the
     * current matrix, would lie completely outside of the current clip. Call
     * this to check if an area you intend to draw into is clipped out (and
     * therefore you can skip making the draw calls).
     *
     * @param left        The left side of the rectangle to compare with the
     *                    current clip
     * @param top         The top of the rectangle to compare with the current
     *                    clip
     * @param right       The right side of the rectangle to compare with the
     *                    current clip
     * @param bottom      The bottom of the rectangle to compare with the
     *                    current clip
     * @param type        {@link Canvas.EdgeType#AA} if the path should be considered antialiased,
     *                    since that means it may affect a larger area (more pixels) than
     *                    non-antialiased ({@link Canvas.EdgeType#BW}).
     * @return            true if the rect (transformed by the canvas' matrix)
     *                    does not intersect with the canvas' clip
     */
    public boolean quickReject(float left, float top, float right, float bottom,
            @NonNull EdgeType type) {
        return nQuickReject(mNativeCanvasWrapper, left, top, right, bottom);
    }
```

![](../assets/images/draw_area.png)