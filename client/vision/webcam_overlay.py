import cv2
from utils.face_detection import detect_faces
from utils.gaze_detection import detect_gaze, draw_iris_overlay, draw_gaze_arrow

cap = None

def init_webcam():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Couldn't open webcam.")
            return False
        print("🎥 Webcam initialized.")
    return True

def get_webcam_frame():
    global cap
    if cap is None or not cap.isOpened():
        return None

    ret, frame = cap.read()
    if not ret:
        return None

    faces = detect_faces(frame)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Face", (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    gaze = detect_gaze(frame)
    draw_iris_overlay(frame, gaze)
    draw_gaze_arrow(frame, gaze)

    if gaze["eye_contact"]:
        cv2.putText(frame, "Eye Contact detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, f"Gaze: {gaze['gaze_direction']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)

    return frame

def release_webcam():
    global cap
    if cap and cap.isOpened():
        cap.release()
        cap = None
        print("🛑 Webcam released.")
