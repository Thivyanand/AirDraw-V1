import cv2
import mediapipe as mp
import math
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

cubes = []
pinch_active = False
dragging_cube = None

SNAP_DISTANCE = 70

# ---------------- Draw Hologram Cube ---------------- #
def draw_hologram_cube(frame, center, size=35, glow=True):
    x, y = center
    s = size

    front = np.array([
        (x-s, y-s),
        (x+s, y-s),
        (x+s, y+s),
        (x-s, y+s)
    ])

    offset = 18
    back = np.array([
        (x-s-offset, y-s-offset),
        (x+s-offset, y-s-offset),
        (x+s-offset, y+s-offset),
        (x-s-offset, y+s-offset)
    ])

    color = (255, 255, 0)  # Cyan hologram

    if glow:
        cv2.polylines(frame, [front], True, color, 3)
        cv2.polylines(frame, [back], True, color, 3)
        for i in range(4):
            cv2.line(frame, tuple(front[i]), tuple(back[i]), color, 3)
    else:
        cv2.polylines(frame, [front], True, color, 1)
        cv2.polylines(frame, [back], True, color, 1)
        for i in range(4):
            cv2.line(frame, tuple(front[i]), tuple(back[i]), color, 1)

# ---------------- Main Loop ---------------- #
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = frame.shape
            lm = hand_landmarks.landmark

            x1 = int(lm[4].x * w)
            y1 = int(lm[4].y * h)
            x2 = int(lm[8].x * w)
            y2 = int(lm[8].y * h)

            distance = math.hypot(x2 - x1, y2 - y1)

            # ---- Pinch START ----
            if distance < 35 and not pinch_active:
                dragging_cube = [x2, y2]
                pinch_active = True

            # ---- While Pinching → Drag with Magnetic Snap ----
            if distance < 35 and pinch_active and dragging_cube:

                snap_x, snap_y = x2, y2

                for cube in cubes:
                    dx = x2 - cube[0]
                    dy = y2 - cube[1]
                    dist = math.hypot(dx, dy)

                    if dist < SNAP_DISTANCE:
                        if abs(dx) > abs(dy):
                            snap_x = cube[0] + (70 if dx > 0 else -70)
                            snap_y = cube[1]
                        else:
                            snap_x = cube[0]
                            snap_y = cube[1] + (70 if dy > 0 else -70)

                dragging_cube[0] = snap_x
                dragging_cube[1] = snap_y

            # ---- Pinch RELEASE → Place ----
            if distance > 40 and pinch_active:
                cubes.append(dragging_cube)
                dragging_cube = None
                pinch_active = False

    # --------- Glow Layer (Draw Once, Blend Once) --------- #
    glow_layer = frame.copy()

    for cube in cubes:
        draw_hologram_cube(glow_layer, cube, glow=True)

    if dragging_cube:
        draw_hologram_cube(glow_layer, dragging_cube, glow=True)

    glow_layer = cv2.GaussianBlur(glow_layer, (15, 15), 0)
    cv2.addWeighted(glow_layer, 0.4, frame, 0.6, 0, frame)

    # --------- Draw Sharp Edges On Top --------- #
    for cube in cubes:
        draw_hologram_cube(frame, cube, glow=False)

    if dragging_cube:
        draw_hologram_cube(frame, dragging_cube, glow=False)

    cv2.imshow("IronMan Style Hologram Cubes", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
