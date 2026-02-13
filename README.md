# AirDraw-V1


# 🧊 AirConstruct – Gesture Controlled 3D Hologram Builder

AirConstruct is a real-time hand-gesture controlled 3D construction system built using:

- 🖐 MediaPipe (hand tracking)
- 🎥 OpenCV (camera rendering)
- 🧮 Custom 3D projection math (no game engine)
- 🧊 Perspective-based 3D cube rendering

This project simulates an Iron-Man style holographic cube construction system using only a webcam.

---

## 🚀 Features

- 🤏 Pinch to spawn & drag cubes
- ✋ Release to place cube
- 🧲 Magnetic snapping system
- 🔄 Full structure rotation using wrist movement
- 📐 True 3D projection math (manual engine)
- ✊ Fist gesture to delete last cube
- 🎥 Clean camera overlay (no OpenGL tint issues)

---

## 🎮 Gesture Controls

| Gesture | Action |
|----------|--------|
| 🤏 Pinch | Spawn & drag cube |
| ✋ Release | Place cube |
| ✊ Fist (0 fingers up) | Delete last cube |
| 🔄 Rotate wrist | Rotate entire structure |
| ✋ Move hand | Move cube in X/Y |
| 🧲 Move near cube | Magnetic snap |

---

## 🧠 How It Works

Instead of using a full 3D engine, this project:

1. Tracks hand landmarks using MediaPipe.
2. Converts hand position into 3D world coordinates.
3. Applies rotation matrices manually.
4. Projects 3D points into 2D screen space using perspective math.
5. Renders hologram-style cube edges over the camera feed.

This makes it a lightweight custom 3D engine built from scratch.

---
##Create Virtual Evironment 

python -m venv venv

venv\Scripts\activate


## 📦 Install Dependencies 
pip install opencv-python mediapipe numpy


##Run 
python airconstruct.py




