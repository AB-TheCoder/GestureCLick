# Computer Vision Crash Course — for Gesture Click

You already know Python and `cv2` basics from `paddle2x.py`. This goes deep on the parts that are new: how a camera frame actually becomes numbers, how MediaPipe finds a hand in those numbers, and the vector math behind matching a gesture.

---

## 1. What a camera frame actually *is*

When you do `cv2.VideoCapture(0)` and read a frame, you don't get a "picture" — you get a 3D array of numbers.

```python
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print(frame.shape)   # e.g. (480, 640, 3)
```

- `480` = height in pixels
- `640` = width in pixels
- `3` = color channels

So `frame` is really a 480×640 grid, and every cell in that grid holds **3 numbers** (0–255 each) for how much Blue, Green, and Red light is at that pixel. That's it — a photo is just a big grid of brightness values. Everything downstream (MediaPipe, OpenCV, PaddleOCR — all of it) is just math done on that grid.

**Important gotcha:** OpenCV stores color as **BGR**, not RGB. Most other libraries (including MediaPipe) expect RGB. You'll see this conversion constantly:

```python
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

Skip this and colors look wrong, or worse — MediaPipe's detector performs poorly because it was trained on RGB images.

---

## 2. What MediaPipe Hands actually does

You don't need to understand the internals to use it, but understanding roughly what's happening will make debugging much easier.

MediaPipe Hands is actually **two models chained together**:

1. **Palm detector** — a small, fast model that scans the whole frame and answers "is there a hand here, and roughly where?" It outputs a bounding box.
2. **Landmark model** — runs *only* on that cropped bounding box (much cheaper than scanning the whole image) and outputs **21 precise (x, y, z) points** on the hand — fingertips, knuckles, wrist.

This two-stage design is why it runs in real time on a laptop — the expensive, precise model only ever looks at a small cropped region, not the full frame.

```python
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,   # False = video stream (uses tracking between frames, faster)
    max_num_hands=1,           # limit to 1 hand for speed and simplicity
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5,
)

results = hands.process(rgb_frame)

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        # hand_landmarks.landmark is a list of 21 points
        for i, lm in enumerate(hand_landmarks.landmark):
            print(i, lm.x, lm.y, lm.z)
```

---

## 3. The 21 landmarks — and why the numbering matters

Each landmark has an index (0–20) that's **always the same body part**, every frame, every hand. This consistency is what makes gesture math possible — landmark 8 is *always* the index fingertip, so you can write rules that work reliably.

The ones you'll actually use for Gesture Click:

| Index | Landmark |
|---|---|
| 0 | Wrist |
| 4 | Thumb tip |
| 8 | Index fingertip |
| 12 | Middle fingertip |
| 16 | Ring fingertip |
| 20 | Pinky fingertip |
| 6 | Index knuckle (PIP joint) |
| 10 | Middle knuckle |

Full 21-point reference: search "MediaPipe hand landmarks diagram" — worth having the image open while you code the gesture rules.

**Critical detail:** `lm.x` and `lm.y` are **normalized 0.0–1.0**, not pixel coordinates. `(0,0)` is the top-left of the frame, `(1,1)` is the bottom-right. To get actual pixel position: `x_px = lm.x * frame_width`. `lm.z` is depth, roughly relative to the wrist — smaller (more negative) means closer to the camera.

---

## 4. The core trick: "is this finger up or down?"

This is the single most useful piece of logic in the whole project. Because MediaPipe hand landmarks are given in a consistent order, you can compare a fingertip's height to its knuckle's height:

```python
def is_finger_up(landmarks, tip_id, pip_id):
    # In image coordinates, SMALLER y = HIGHER on screen (y grows downward)
    return landmarks[tip_id].y < landmarks[pip_id].y

index_up = is_finger_up(landmarks, tip_id=8, pip_id=6)
middle_up = is_finger_up(landmarks, tip_id=12, pip_id=10)
```

A peace sign is just: `index_up and middle_up and not ring_up and not pinky_up`. That's genuinely most of what preset-gesture apps like the ones we found are doing under the hood — simple, readable rules on top of landmark positions.

Thumb is the one exception — because it moves sideways more than up/down, you usually compare its **x** position instead, relative to which hand it is (mirrored for left vs right).

---

## 5. Why "just compare coordinates" breaks — and the fix (normalization)

Here's the problem you'll hit almost immediately: a hand held close to the camera and the same hand held far away produce very different raw coordinate values, even though it's the *same gesture*. Distance and hand size distort everything.

The fix — and this is the same principle your `paddle2x.py` OCR pipeline uses when it resizes/normalizes images before reading them — is to make your gesture data **scale-invariant** before comparing it:

```python
import numpy as np

def normalize_landmarks(landmarks):
    points = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])

    # 1. Make everything relative to the wrist (landmark 0)
    #    so position in the frame no longer matters
    wrist = points[0]
    points = points - wrist

    # 2. Scale so overall hand size doesn't matter
    #    (divide by the distance from wrist to middle knuckle, a stable reference)
    scale = np.linalg.norm(points[9])  # landmark 9 = middle finger knuckle (MCP)
    if scale > 0:
        points = points / scale

    return points
```

After this, a peace sign held close to the camera and a peace sign held far away produce **nearly identical numbers**. This is what makes custom gesture *matching* (not just hardcoded rules) actually work.

---

## 6. Custom gesture matching — nearest-neighbor with Euclidean distance

This is your actual differentiator over the built-in phone features. Instead of hardcoding "peace sign = these specific fingers up," you let the user show you *any* gesture, save its normalized landmark shape, and later compare new frames against it.

```python
def euclidean_distance(a, b):
    # a and b are both normalized 21x3 landmark arrays
    return np.linalg.norm(a.flatten() - b.flatten())

def match_gesture(current_landmarks, saved_gestures, threshold=0.15):
    current_norm = normalize_landmarks(current_landmarks)
    best_match = None
    best_distance = float("inf")

    for name, saved_norm in saved_gestures.items():
        dist = euclidean_distance(current_norm, saved_norm)
        if dist < best_distance:
            best_distance = dist
            best_match = name

    if best_distance < threshold:
        return best_match
    return None  # nothing matched closely enough
```

`threshold` is a number you'll tune by testing — too low and real gestures won't match (too strict), too high and unrelated hand shapes trigger false positives. This is genuinely the same "how much noise before it stops being reliable" tradeoff you dealt with in your OCR confidence thresholds (`drop_score=0.45` in `paddle2x.py` is doing the exact same job for text).

---

## 7. Temporal logic — a gesture needs to be *held*, not just glimpsed

A single matching frame isn't enough — a hand passing through a peace-sign-like shape for one frame while moving would falsely trigger a capture. You need a small state machine that tracks *how long* a gesture has been held:

```python
import time

class GestureState:
    def __init__(self, hold_seconds=0.7, cooldown_seconds=2.0):
        self.current_gesture = None
        self.gesture_start_time = None
        self.hold_seconds = hold_seconds
        self.last_trigger_time = 0
        self.cooldown_seconds = cooldown_seconds

    def update(self, detected_gesture):
        now = time.time()

        # Still in cooldown after the last capture — ignore everything
        if now - self.last_trigger_time < self.cooldown_seconds:
            return None

        if detected_gesture != self.current_gesture:
            # Gesture changed (or lost) — reset the timer
            self.current_gesture = detected_gesture
            self.gesture_start_time = now
            return None

        if detected_gesture is not None and (now - self.gesture_start_time) >= self.hold_seconds:
            self.last_trigger_time = now
            self.current_gesture = None  # reset so it doesn't fire again immediately
            return detected_gesture  # TRIGGER!

        return None
```

This gives you three tunable numbers that directly shape how the product *feels*: `hold_seconds` (how deliberate a gesture must be — too short and accidents happen, too long and it feels laggy), and `cooldown_seconds` (prevents rapid-fire duplicate captures right after one fires).

---

## 8. Putting the whole loop together

```python
state = GestureState(hold_seconds=0.7, cooldown_seconds=2.0)
saved_gestures = load_saved_gestures()  # from your JSON/pickle files

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    detected = None
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        detected = match_gesture(landmarks, saved_gestures)

    triggered = state.update(detected)
    if triggered:
        capture_photo(frame, gesture_name=triggered)

    cv2.imshow("Gesture Click", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

Every piece maps to a file in your project structure: the camera loop → `camera.py`, `hands.process()` → `detector.py`, `match_gesture()` → `gestures.py`, `GestureState` → also `gestures.py` or its own module, `capture_photo()` → `capture.py`.

---

## 9. Why frame rate matters here (and a common trap)

`hands.process()` is the expensive line in that loop — it's running a neural network on every single frame. On a slower laptop, this can drop your effective frame rate significantly, which directly hurts gesture detection reliability (fewer samples = harder to reliably measure "held for 0.7 seconds").

Two things that help without needing better hardware:
- **Downscale the frame before detection** (`cv2.resize()` to e.g. 640×480 or smaller) — MediaPipe doesn't need full resolution to find a hand, only to be precise about landmarks, and even then it's already working on a small cropped region internally.
- **`static_image_mode=False`** (already in the snippet above) — this tells MediaPipe to use cheaper frame-to-frame tracking instead of running full detection every single frame, which is a large speed win for video.

---

## 10. Cheat sheet — key ideas to remember

| Concept | What it means in plain terms |
|---|---|
| Frame | A grid of BGR numbers, not a "picture" |
| Normalized coordinates | `lm.x`/`lm.y` are 0–1, not pixels — multiply by width/height to get pixels |
| Landmark index | A fixed ID (0–20) that always means the same hand part |
| Normalization (wrist + scale) | Makes gestures comparable regardless of hand size/distance from camera |
| Euclidean distance | A single number measuring "how different are these two hand shapes" |
| Threshold | The cutoff distance below which you call it a match — tune by testing |
| Hold time | Prevents a gesture glimpsed for one frame from falsely triggering |
| Cooldown | Prevents the same gesture firing repeatedly right after it triggers |

---

## Your task

Build it in this order, testing each piece before moving to the next:

1. Get the raw camera loop showing your webcam feed (`cv2.imshow`)
2. Add MediaPipe and draw the 21 landmarks on screen as dots (MediaPipe has a built-in `mp_drawing.draw_landmarks()` helper for this — great for seeing what the model sees)
3. Write `is_finger_up()` and hardcode one preset gesture (peace sign) — get a print statement firing when detected
4. Add the hold-time state machine so it only triggers once per deliberate gesture
5. Wire that trigger to `cv2.imwrite()` to actually save a photo
6. Only once that whole loop works reliably, build the normalization + custom-gesture-training piece

Post your code as you build each piece — happy to review rather than hand you the finished thing.