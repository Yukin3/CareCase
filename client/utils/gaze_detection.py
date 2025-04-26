import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,  # Enables iris landmarks
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Iris landmark indexes (right/left eye center)
RIGHT_IRIS = [474, 475, 476, 477]
LEFT_IRIS = [469, 470, 471, 472]

def detect_gaze(frame):
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    h, w = frame.shape[:2]

    if not results.multi_face_landmarks:
        return {"eye_contact": False, "gaze_direction": "unknown", "landmarks": {}}

    face_landmarks = results.multi_face_landmarks[0]

    # Convert landmarks to pixel coordinates
    def to_px(landmark): return int(landmark.x * w), int(landmark.y * h)

    # Get left/right iris centers
    left_iris = [to_px(face_landmarks.landmark[i]) for i in LEFT_IRIS]
    right_iris = [to_px(face_landmarks.landmark[i]) for i in RIGHT_IRIS]

    # Use center of iris points as approximation
    def center(points):
        x = sum(p[0] for p in points) // len(points)
        y = sum(p[1] for p in points) // len(points)
        return (x, y)

    left_center = center(left_iris)
    right_center = center(right_iris)

    # Estimate gaze direction by relative iris position
    # We'll use a simple method: if iris is left of eye center → looking right
    left_eye_corner = to_px(face_landmarks.landmark[33])  # outer left
    right_eye_corner = to_px(face_landmarks.landmark[263])  # outer right

    eye_width = right_eye_corner[0] - left_eye_corner[0]
    eye_center_x = left_eye_corner[0] + eye_width // 2
    gaze_x = (left_center[0] + right_center[0]) // 2

    offset_ratio = (gaze_x - eye_center_x) / (eye_width / 2)

    if abs(offset_ratio) < 0.3:
        gaze_direction = "center"
        eye_contact = True
    elif offset_ratio < -0.3:
        gaze_direction = "left"
        eye_contact = False
    else:
        gaze_direction = "right"
        eye_contact = False

    return {
        "eye_contact": eye_contact,
        "gaze_direction": gaze_direction,
        "landmarks": {
            "left_iris": left_iris,
            "right_iris": right_iris
        }
    }


# 🌀 Optional visualization helper
def draw_iris_overlay(frame, gaze):
    landmarks = gaze.get("landmarks", {})
    for (x, y) in landmarks.get("left_iris", []):
        cv2.circle(frame, (x, y), 1, (255, 255, 0), 1)
    for (x, y) in landmarks.get("right_iris", []):
        cv2.circle(frame, (x, y), 1, (255, 255, 0), 1)

#TODO: FIX gaze arrow and tracking
# ➡️ Optional vector arrow helper
def draw_gaze_arrow(frame, gaze):
    landmarks = gaze.get("landmarks", {})
    center = landmarks.get("right_center")
    if center is None:
        return  # Don't draw if iris center isn't available
    direction_map = {
        "left": (-40, 0),
        "right": (40, 0),
        "center": (0, 0)
    }
    dx, dy = direction_map.get(gaze.get("gaze_direction", "center"), (0, 0))
    end_point = (center[0] + dx, center[1] + dy)
    cv2.arrowedLine(frame, center, end_point, (0, 255, 255), 2, tipLength=0.2)
