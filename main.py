import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ---------------------- PyCaw Setup ----------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume)).QueryInterface(IAudioEndpointVolume)

# Get min and max dB values for clamping
min_vol, max_vol, _ = volume.GetVolumeRange()

# ------------------- MediaPipe Setup ---------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ------------------- Camera Setup ------------------------
cap = cv2.VideoCapture(0)
flip_cam = True

# ------------------- Lock Control -----------------------
volume_locked = False
LOCK_REGION_SIZE = 60  # size of the visual lock box (pixels)

# ------------------- Main Loop ---------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if flip_cam:
        frame = cv2.flip(frame, 1)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Thumb tip (4) and Index tip (8)
            x1, y1 = int(handLms.landmark[4].x * frame.shape[1]), int(handLms.landmark[4].y * frame.shape[0])
            x2, y2 = int(handLms.landmark[8].x * frame.shape[1]), int(handLms.landmark[8].y * frame.shape[0])

            cv2.circle(frame, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # ----------------- Finger Up/Down Lock -----------------
            # Middle finger tip = 12, PIP = 10
            mid_x, mid_y = int(handLms.landmark[12].x * frame.shape[1]), int(handLms.landmark[12].y * frame.shape[0])
            middle_up = handLms.landmark[12].y < handLms.landmark[10].y
            volume_locked = not middle_up  # True if middle finger down

            # ----------------- Volume Control -------------------
            length = hypot(x2 - x1, y2 - y1)
            if not volume_locked:
                vol_target = np.interp(length, [30, 200], [min_vol, max_vol])
                try:
                    current_vol = volume.GetMasterVolumeLevel()
                except AttributeError:
                    current_vol = min_vol

                # Smooth transition
                vol = current_vol + 0.2 * (vol_target - current_vol)

                # Clamp
                vol = max(min(vol, max_vol), min_vol)
                volume.SetMasterVolumeLevel(vol, None)

            # ----------------- Visuals --------------------------
            # Volume percentage
            vol_percent = np.interp(length, [30, 200], [0, 100])
            cv2.putText(frame, f'Vol: {int(vol_percent)} %', (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            # Lock status
            status = 'Locked' if volume_locked else 'Unlocked'
            cv2.putText(frame, status, (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

            # Highlight lock region around middle finger tip
            color = (0, 0, 255) if volume_locked else (0, 255, 0)  # Red = locked, Green = unlocked
            cv2.rectangle(frame,
                          (mid_x - LOCK_REGION_SIZE // 2, mid_y - LOCK_REGION_SIZE // 2),
                          (mid_x + LOCK_REGION_SIZE // 2, mid_y + LOCK_REGION_SIZE // 2),
                          color, 2)

    cv2.imshow("Hand Gesture Volume", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
