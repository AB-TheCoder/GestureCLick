# OpenCV Basics Reference

Core functions, install instructions, and code snippets for quick lookup while building Gesture Click.

---

## 1. Install

```bash
pip install opencv-python==4.13.0 numpy --break-system-packages
```

```python
import cv2
import numpy as np
```

---

## 2. Reading, Displaying, and Saving Images

**Read an image**
```python
image = cv2.imread("photo.jpg")
if image is None:
    raise ValueError("Could not read image")

print(image.shape)   # (height, width, channels)
```

**Show an image in a window**
```python
cv2.imshow("Window Title", image)
cv2.waitKey(0)          # 0 = wait forever for a keypress
cv2.destroyAllWindows()
```

**Save an image**
```python
cv2.imwrite("output.jpg", image)
```

---

## 3. Color Conversions

OpenCV stores color as **BGR** by default, not RGB. Convert before using other libraries (e.g. MediaPipe expects RGB).

```python
gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
rgb   = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
hsv   = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
```

---

## 4. Resizing and Cropping

**Resize**
```python
resized = cv2.resize(image, (640, 480), interpolation=cv2.INTER_CUBIC)

# Interpolation choices:
#  INTER_NEAREST  - fastest, blockiest
#  INTER_LINEAR   - good default, fast
#  INTER_CUBIC    - smoother, slower, best for enlarging
```

**Crop** (just NumPy array slicing — no special function needed)
```python
cropped = image[y1:y2, x1:x2]
```

---

## 5. Drawing on Images

```python
cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
cv2.circle(image, (cx, cy), radius=20, color=(255, 0, 0), thickness=2)
cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
cv2.putText(image, "Hello", (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2)

# Note: colors are (B, G, R) tuples, and drawing happens IN PLACE
```

---

## 6. Blurring and Sharpening

```python
blur = cv2.GaussianBlur(image, (5, 5), sigmaX=0)   # kernel size must be odd
blur = cv2.medianBlur(image, 5)                     # good for salt-and-pepper noise

sharpen_kernel = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])
sharp = cv2.filter2D(image, -1, sharpen_kernel)
```

---

## 7. Thresholding (Binarizing)

**Global threshold**
```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

**Adaptive threshold** (better for uneven lighting)
```python
binary = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    blockSize=31,   # must be odd — size of local neighborhood
    C=10,           # constant subtracted from local mean
)
```

---

## 8. Morphological Operations

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

eroded  = cv2.erode(binary, kernel, iterations=1)   # shrinks white regions
dilated = cv2.dilate(binary, kernel, iterations=1)  # grows white regions
opened  = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)   # remove noise
closed  = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)  # fill small gaps
```

---

## 9. Edge Detection

```python
edges = cv2.Canny(gray, threshold1=100, threshold2=200)

# threshold1/threshold2 control sensitivity:
# lower values = more edges detected (including noise)
```

---

## 10. Contours (Shape Outlines)

```python
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    area = cv2.contourArea(c)
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
```

---

## 11. Rotation

```python
h, w = image.shape[:2]
matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle=15, scale=1.0)
rotated = cv2.warpAffine(image, matrix, (w, h))
```

---

## 12. Camera / Video Capture

```python
cap = cv2.VideoCapture(0)   # 0 = default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

> **Note:** `cap.read()` is blocking — it waits for the OS camera driver to hand over the next frame. A slow camera or busy USB bus will slow down your whole loop.

**Save a video**
```python
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter("output.mp4", fourcc, 20.0, (640, 480))

writer.write(frame)   # call this each loop iteration while recording
writer.release()      # call once when done
```

---

## 13. Common Gotchas

- `imread()` returns `None` on a bad path — it does **NOT** raise an error. Always check for `None`.
- Colors are **BGR** by default, not RGB — convert before using other libraries.
- Kernel sizes for blur/threshold must be **odd numbers** (3, 5, 7, 9...).
- Drawing functions (`rectangle`, `circle`, `putText`) modify the image **in place** and also return it.
- `waitKey(1)` inside a loop is required — without it, `imshow()` windows won't refresh.
- Never loop over pixels manually in Python — always use a `cv2`/NumPy vectorized function instead.

---

## 14. Quick Reference Table

| Task | Function |
|---|---|
| Read image | `cv2.imread(path)` |
| Show image | `cv2.imshow(name, image)` |
| Save image | `cv2.imwrite(path, image)` |
| Convert color | `cv2.cvtColor(image, code)` |
| Resize | `cv2.resize(image, size, interpolation=...)` |
| Blur | `cv2.GaussianBlur(image, ksize, sigmaX)` |
| Sharpen / custom filter | `cv2.filter2D(image, -1, kernel)` |
| Threshold (global) | `cv2.threshold(gray, val, 255, type)` |
| Threshold (adaptive) | `cv2.adaptiveThreshold(gray, ...)` |
| Erode / Dilate | `cv2.erode()` / `cv2.dilate()` |
| Open / Close | `cv2.morphologyEx(image, type, kernel)` |
| Edge detection | `cv2.Canny(gray, t1, t2)` |
| Find contours | `cv2.findContours(binary, mode, method)` |
| Rotate | `cv2.warpAffine(image, matrix, size)` |
| Open camera | `cv2.VideoCapture(0)` |
| Read camera frame | `cap.read()` |
