Omni Focus — Eye-Controlled Mouse using MediaPipe & Python

A lightweight, software-only eye-tracking mouse system that uses a normal webcam and MediaPipe FaceMesh to control the system cursor, perform clicks using blinks, and scroll using head tilt.

📌 Features

🎯 Eye-controlled cursor movement using iris tracking

👀 Blink-based clicking

Left blink → Left Click

Right blink → Right Click

Both eyes blink → Scroll Down

⬆⬇ Head tilt scrolling

Look up → Scroll Up

Look down → Scroll Down

🖥 Works on any system using a regular webcam

🧠 Powered by MediaPipe FaceMesh, OpenCV, and PyAutoGUI

📂 File Overview

This project contains a single Python script:

omni_focus_eye_mouse.py — Main script for eye-tracking mouse control

🛠 Requirements

Install the required Python packages:

pip install opencv-python mediapipe pyautogui


Note: On Windows, PyAutoGUI may need pillow preinstalled:

pip install pillow

▶️ How It Works
1. Cursor Movement

Uses iris landmark point 476 to map real-time eye movement to screen coordinates:

ix = int(lm[476].x * w)
iy = int(lm[476].y * h)
mx = int(ix / w * Wscr)
my = int(iy / h * Hscr)
pyautogui.moveTo(mx, my)

2. Blink Detection

Checks vertical eyelid distance for left and right eye:

def is_blink(landmarks, upper_idx, lower_idx, threshold=0.01):
    return abs(landmarks[upper_idx].y - landmarks[lower_idx].y) < threshold


Blink → Action mapping:

Action	Trigger
Left Click	Left eye blink
Right Click	Right eye blink
Scroll Down	Both eyes blink
Scroll Up	Head tilt upward

A cooldown of 1.5 seconds prevents repeated accidental clicks.

3. Head Tilt Scroll

Uses nose landmark (index 1) to detect head tilt:

if lm[1].y < 0.35:
    pyautogui.scroll(300)
elif lm[1].y > 0.65:
    pyautogui.scroll(-300)

👁 Landmark Visualization

Left eye points → Yellow

Right eye points → Red

These help with debugging accuracy and calibration.

✨ Running the Project

Just run:

python omni_focus_eye_mouse.py


Controls:

ESC → Exit the program

Look → Move cursor

Blink → Click

Tilt head → Scroll

🧩 Code Structure

The script includes:

Webcam Capture

FaceMesh Processing

Iris Landmark Tracking

Eye Blink Detection

Cursor Movement

Click Actions

Optical Feedback (landmarks drawn on video feed)

📌 Notes & Tips

Use good lighting for accurate landmark detection

Sit around 40–70 cm from the webcam

If cursor movement feels too fast/slow, adjust mapping scale

Cooldown time can be modified depending on user preference

📄 License

This project is free to use for educational and research purposes.
