## Android源码阅读遗留问题

### ImageDecoder.java(Android 9)

```java
    File file = new File(filePath);
    // FileSource
    ImageDecoder.Source source = ImageDecoder.createSource(file);
    Bitmap drawable = ImageDecoder.decodeBitmap(source);
```
FileSource被强转成了InputStreamSource：
```java
/**
 *  Class for decoding images as {@link Bitmap}s or {@link Drawable}s.
 */
public final class ImageDecoder implements AutoCloseable {

    /**
     *  Create a {@link Bitmap} from a {@code Source}.
     *
     *  @param src representing the encoded image.
     *  @param listener for learning the {@link ImageInfo} and changing any
     *      default settings on the {@code ImageDecoder}. If not {@code null},
     *      this will be called on the same thread as {@code decodeBitmap}
     *      before that method returns.
     *  @return Bitmap containing the image.
     *  @throws IOException if {@code src} is not found, is an unsupported
     *      format, or cannot be decoded for any reason.
     */
    @NonNull
    public static Bitmap decodeBitmap(@NonNull Source src,
            @Nullable OnHeaderDecodedListener listener) throws IOException {
        TypedValue value = new TypedValue();
        value.density = src.getDensity();
        ImageDecoder decoder = src.createImageDecoder();
        if (listener != null) {
            listener.onHeaderDecoded(decoder, new ImageInfo(decoder), src);
        }
        return BitmapFactory.decodeResourceStream(src.getResources(), value,
                ((InputStreamSource) src).mInputStream, decoder.mOutPaddingRect, null);
    }
}
```

而FileSource和InputStreamSource并无继承关系：
```java
    private static class FileSource extends Source {
        FileSource(@NonNull File file) {
            mFile = file;
        }

        private final File mFile;

        @Override
        public ImageDecoder createImageDecoder() throws IOException {
            return new ImageDecoder();
        }
    }
```

```java
    /**
     * For backwards compatibility, this does *not* close the InputStream.
     */
    private static class InputStreamSource extends Source {
        InputStreamSource(Resources res, InputStream is, int inputDensity) {
            if (is == null) {
                throw new IllegalArgumentException("The InputStream cannot be null");
            }
            mResources = res;
            mInputStream = is;
            mInputDensity = res != null ? inputDensity : Bitmap.DENSITY_NONE;
        }

        final Resources mResources;
        InputStream mInputStream;
        final int mInputDensity;

        @Override
        public Resources getResources() { return mResources; }

        @Override
        public int getDensity() { return mInputDensity; }

        @Override
        public ImageDecoder createImageDecoder() throws IOException {
            return new ImageDecoder();
        }
    }
```

且Android Studio关联的源码和Googlesource网站上的源码不一致：[https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/graphics/java/android/graphics/ImageDecoder.java](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/graphics/java/android/graphics/ImageDecoder.java)：
```java
/**
 *  <p>A class for converting encoded images (like {@code PNG}, {@code JPEG},
 *  {@code WEBP}, {@code GIF}, or {@code HEIF}) into {@link Drawable} or
 *  {@link Bitmap} objects.
 *
 *  <p>To use it, first create a {@link Source Source} using one of the
 *  {@code createSource} overloads. For example, to decode from a {@link File}, call
 *  {@link #createSource(File)} and pass the result to {@link #decodeDrawable(Source)}
 *  or {@link #decodeBitmap(Source)}:
 *
 *  <pre class="prettyprint">
 *  File file = new File(...);
 *  ImageDecoder.Source source = ImageDecoder.createSource(file);
 *  Drawable drawable = ImageDecoder.decodeDrawable(source);
 *  </pre>
 *
 *  <p>To change the default settings, pass the {@link Source Source} and an
 *  {@link OnHeaderDecodedListener OnHeaderDecodedListener} to
 *  {@link #decodeDrawable(Source, OnHeaderDecodedListener)} or
 *  {@link #decodeBitmap(Source, OnHeaderDecodedListener)}. For example, to
 *  create a sampled image with half the width and height of the original image,
 *  call {@link #setTargetSampleSize setTargetSampleSize(2)} inside
 *  {@link OnHeaderDecodedListener#onHeaderDecoded onHeaderDecoded}:
 *
 *  <pre class="prettyprint">
 *  OnHeaderDecodedListener listener = new OnHeaderDecodedListener() {
 *      public void onHeaderDecoded(ImageDecoder decoder, ImageInfo info, Source source) {
 *          decoder.setTargetSampleSize(2);
 *      }
 *  };
 *  Drawable drawable = ImageDecoder.decodeDrawable(source, listener);
 *  </pre>
 *
 *  <p>The {@link ImageInfo ImageInfo} contains information about the encoded image, like
 *  its width and height, and the {@link Source Source} can be used to match to a particular
 *  {@link Source Source} if a single {@link OnHeaderDecodedListener OnHeaderDecodedListener}
 *  is used with multiple {@link Source Source} objects.
 *
 *  <p>The {@link OnHeaderDecodedListener OnHeaderDecodedListener} can also be implemented
 *  as a lambda:
 *
 *  <pre class="prettyprint">
 *  Drawable drawable = ImageDecoder.decodeDrawable(source, (decoder, info, src) -&gt; {
 *      decoder.setTargetSampleSize(2);
 *  });
 *  </pre>
 *
 *  <p>If the encoded image is an animated {@code GIF} or {@code WEBP},
 *  {@link #decodeDrawable decodeDrawable} will return an {@link AnimatedImageDrawable}. To
 *  start its animation, call {@link AnimatedImageDrawable#start AnimatedImageDrawable.start()}:
 *
 *  <pre class="prettyprint">
 *  Drawable drawable = ImageDecoder.decodeDrawable(source);
 *  if (drawable instanceof AnimatedImageDrawable) {
 *      ((AnimatedImageDrawable) drawable).start();
 *  }
 *  </pre>
 *
 *  <p>By default, a {@link Bitmap} created by {@link ImageDecoder} (including
 *  one that is inside a {@link Drawable}) will be immutable (i.e.
 *  {@link Bitmap#isMutable Bitmap.isMutable()} returns {@code false}), and it
 *  will typically have {@code Config} {@link Bitmap.Config#HARDWARE}. Although
 *  these properties can be changed with {@link #setMutableRequired setMutableRequired(true)}
 *  (which is only compatible with {@link #decodeBitmap(Source)} and
 *  {@link #decodeBitmap(Source, OnHeaderDecodedListener)}) and {@link #setAllocator},
 *  it is also possible to apply custom effects regardless of the mutability of
 *  the final returned object by passing a {@link PostProcessor} to
 *  {@link #setPostProcessor setPostProcessor}. A {@link PostProcessor} can also be a lambda:
 *
 *  <pre class="prettyprint">
 *  Drawable drawable = ImageDecoder.decodeDrawable(source, (decoder, info, src) -&gt; {
 *      decoder.setPostProcessor((canvas) -&gt; {
 *              // This will create rounded corners.
 *              Path path = new Path();
 *              path.setFillType(Path.FillType.INVERSE_EVEN_ODD);
 *              int width = canvas.getWidth();
 *              int height = canvas.getHeight();
 *              path.addRoundRect(0, 0, width, height, 20, 20, Path.Direction.CW);
 *              Paint paint = new Paint();
 *              paint.setAntiAlias(true);
 *              paint.setColor(Color.TRANSPARENT);
 *              paint.setXfermode(new PorterDuffXfermode(PorterDuff.Mode.SRC));
 *              canvas.drawPath(path, paint);
 *              return PixelFormat.TRANSLUCENT;
 *      });
 *  });
 *  </pre>
 *
 *  <p>If the encoded image is incomplete or contains an error, or if an
 *  {@link Exception} occurs during decoding, a {@link DecodeException DecodeException}
 *  will be thrown. In some cases, the {@link ImageDecoder} may have decoded part of
 *  the image. In order to display the partial image, an
 *  {@link OnPartialImageListener OnPartialImageListener} must be passed to
 *  {@link #setOnPartialImageListener setOnPartialImageListener}. For example:
 *
 *  <pre class="prettyprint">
 *  Drawable drawable = ImageDecoder.decodeDrawable(source, (decoder, info, src) -&gt; {
 *      decoder.setOnPartialImageListener((DecodeException e) -&gt; {
 *              // Returning true indicates to create a Drawable or Bitmap even
 *              // if the whole image could not be decoded. Any remaining lines
 *              // will be blank.
 *              return true;
 *      });
 *  });
 *  </pre>
 */
public final class ImageDecoder implements AutoCloseable {

    /**
     *  Create a {@link Bitmap} from a {@code Source}.
     *
     *  @param src representing the encoded image.
     *  @param listener for learning the {@link ImageInfo ImageInfo} and changing any
     *      default settings on the {@code ImageDecoder}. This will be called on
     *      the same thread as {@code decodeBitmap} before that method returns.
     *      This is required in order to change any of the default settings.
     *  @return Bitmap containing the image.
     *  @throws IOException if {@code src} is not found, is an unsupported
     *      format, or cannot be decoded for any reason.
     */
    @WorkerThread
    @NonNull
    public static Bitmap decodeBitmap(@NonNull Source src,
            @NonNull OnHeaderDecodedListener listener) throws IOException {
        if (listener == null) {
            throw new IllegalArgumentException("listener cannot be null! "
                    + "Use decodeBitmap(Source) to not have a listener");
        }
        return decodeBitmapImpl(src, listener);
    }
    
    @WorkerThread
    @NonNull
    private static Bitmap decodeBitmapImpl(@NonNull Source src,
            @Nullable OnHeaderDecodedListener listener) throws IOException {
        try (ImageDecoder decoder = src.createImageDecoder()) {
            decoder.mSource = src;
            decoder.callHeaderDecoded(listener, src);
            // this call potentially manipulates the decoder so it must be performed prior to
            // decoding the bitmap
            final int srcDensity = decoder.computeDensity(src);
            Bitmap bm = decoder.decodeBitmapInternal();
            bm.setDensity(srcDensity);
            Rect padding = decoder.mOutPaddingRect;
            if (padding != null) {
                byte[] np = bm.getNinePatchChunk();
                if (np != null && NinePatch.isNinePatchChunk(np)) {
                    nGetPadding(decoder.mNativePtr, padding);
                }
            }
            return bm;
        }
    }
}
```

