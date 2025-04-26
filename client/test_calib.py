import cv2
import mediapipe as mp
import numpy as np
import time
import json

# --- Setup Mediapipe ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# --- Calibration Dots ---
screen_w, screen_h = 800, 480  # adjust based on current display
calibration_points = [
    (100, 100), (screen_w // 2, 100), (screen_w - 100, 100),
    (100, screen_h // 2), (screen_w // 2, screen_h // 2), (screen_w - 100, screen_h // 2),
    (100, screen_h - 100), (screen_w // 2, screen_h - 100), (screen_w - 100, screen_h - 100),
]

collected_data = []

# --- Open Webcam ---
cap = cv2.VideoCapture(0)

def draw_dot(window, pos, wait_time=2):
    img = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
    cv2.circle(img, pos, 10, (0, 255, 0), -1)
    cv2.imshow(window, img)
    cv2.waitKey(wait_time * 1000)

def get_iris_center(landmarks, w, h):
    # Iris landmark index (right eye): 474–475
    x = int(landmarks[474].x * w)
    y = int(landmarks[474].y * h)
    return (x, y)

# --- Run Calibration ---
window = "Calibration"
cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

for point in calibration_points:
    draw_dot(window, point)
    success, frame = cap.read()
    if not success:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape
        iris_center = get_iris_center(landmarks, w, h)

        collected_data.append({
            "target": point,
            "iris": iris_center
        })

cv2.destroyAllWindows()
cap.release()

# Save to file
with open("gaze_calibration_data.json", "w") as f:
    json.dump(collected_data, f, indent=2)

print("Calibration complete ✅ Data saved to gaze_calibration_data.json")
