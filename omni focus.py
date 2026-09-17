import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe FaceMesh
mp_face = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cap = cv2.VideoCapture(0)
Wscr, Hscr = pyautogui.size()

# Helper function to check blink by eyelid distance
def is_blink(landmarks, upper_idx, lower_idx, threshold=0.01):
    return abs(landmarks[upper_idx].y - landmarks[lower_idx].y) < threshold

last_action_time = 0
cooldown = 1.5   # seconds to avoid repeated actions

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)   # mirror effect
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face.process(rgb)

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark

        # -------- Cursor movement (using right iris landmark 476) --------
        ix = int(lm[476].x * w)
        iy = int(lm[476].y * h)
        mx = int(ix / w * Wscr)
        my = int(iy / h * Hscr)
        pyautogui.moveTo(mx, my)

        # -------- Blink detection --------
        left_blink = is_blink(lm, 159, 145)   # left eye
        right_blink = is_blink(lm, 386, 374)  # right eye

        # -------- Draw landmarks (points only) --------
      # Left eye (2 points: yellow, smaller size)
        for idx in [145, 159]:
            x = int(lm[idx].x * w)
            y = int(lm[idx].y * h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)  # yellow points

# Right eye (4 points: red, smaller size)
        for idx in [386, 374, 362, 263]:
            x = int(lm[idx].x * w)
            y = int(lm[idx].y * h)
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # red points


        # -------- Actions with cooldown --------
        if time.time() - last_action_time > cooldown:
            if left_blink and not right_blink:
                pyautogui.click()   # Left click
                print("Left Click")
                last_action_time = time.time()

            elif right_blink and not left_blink:
                pyautogui.click(button='right')   # Right click
                print("Right Click")
                last_action_time = time.time()

            elif left_blink and right_blink:
                pyautogui.scroll(-300)   # Scroll down
                print("Scroll Down")
                last_action_time = time.time()

        # -------- Optional: head tilt scroll --------
        if lm[1].y < 0.35:   # looking up
            pyautogui.scroll(300)   # Scroll up
            print("Scroll Up")
        elif lm[1].y > 0.65: # looking down
            pyautogui.scroll(-300)  # Scroll down
            print("Scroll Down (head tilt)")

    cv2.imshow("Omni Focus Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
