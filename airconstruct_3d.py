import cv2
import mediapipe as mp
import numpy as np
import math

# -------- MediaPipe --------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

# -------- 3D World --------
cubes = []
pinch_active = False
dragging_cube = None

WORLD_SCALE = 3
CUBE_SIZE = 0.5
SNAP_DISTANCE = 1.0

scene_rot_x = 0
scene_rot_y = 0

# -------- 3D Cube Vertices --------
cube_vertices = np.array([
    [-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
    [-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]
])

edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

# -------- 3D Rotation --------
def rotate_point(point, rx, ry):
    x, y, z = point

    # Rotate X
    cosx, sinx = math.cos(rx), math.sin(rx)
    y, z = y*cosx - z*sinx, y*sinx + z*cosx

    # Rotate Y
    cosy, siny = math.cos(ry), math.sin(ry)
    x, z = x*cosy + z*siny, -x*siny + z*cosy

    return np.array([x, y, z])

# -------- Projection --------
def project(point, width, height):
    fov = 400
    z = point[2] + 5
    if z == 0:
        z = 0.1
    factor = fov / z
    x = int(point[0] * factor + width/2)
    y = int(-point[1] * factor + height/2)
    return (x, y)

# -------- Snap --------
def snap_position(pos):
    for cube in cubes:
        dist = np.linalg.norm(np.array(pos) - np.array(cube))
        if dist < SNAP_DISTANCE:
            return [cube[0] + 1, cube[1], cube[2]]
    return pos

# -------- Main Loop --------
while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            lm = hand_landmarks.landmark

            # Hand → World coords
            x = (lm[8].x - 0.5) * WORLD_SCALE * 4
            y = -(lm[8].y - 0.5) * WORLD_SCALE * 3
            z = -2

            # Wrist rotation
            scene_rot_x = (lm[5].y - lm[0].y) * 3
            scene_rot_y = (lm[5].x - lm[0].x) * 3

            # Pinch
            pinch = math.hypot(
                lm[4].x - lm[8].x,
                lm[4].y - lm[8].y
            )

            if pinch < 0.05 and not pinch_active:
                dragging_cube = [x, y, z]
                pinch_active = True

            if pinch < 0.05 and pinch_active:
                dragging_cube = snap_position([x, y, z])

            if pinch > 0.06 and pinch_active:
                cubes.append(dragging_cube)
                dragging_cube = None
                pinch_active = False

            # Delete (fist)
            fingers = [
                lm[8].y < lm[6].y,
                lm[12].y < lm[10].y,
                lm[16].y < lm[14].y,
                lm[20].y < lm[18].y
            ]
            if fingers.count(True) == 0 and len(cubes) > 0:
                cubes.pop()

    # -------- Draw Scene --------
    for cube in cubes + ([dragging_cube] if dragging_cube else []):
        if cube is None:
            continue

        for edge in edges:
            points = []
            for vertex in edge:
                vert = cube_vertices[vertex] * CUBE_SIZE
                vert = vert + cube
                vert = rotate_point(vert, scene_rot_x, scene_rot_y)
                points.append(project(vert, w, h))

            cv2.line(frame, points[0], points[1], (255,255,0), 2)

    cv2.imshow("AirConstruct Clean 3D", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
