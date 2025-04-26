import cv2
import time
import threading
from fer import FER
from datetime import datetime

# 🔁 Emotion log that preceptor can access
_expression_log = []

# 🧠 Emotion detector (MTCNN optional)
_detector = FER(mtcnn=True)  # mtcnn=False = faster, mtcnn=True = more accurate

# 🧪 Loop control
_running = False
_thread = None

def _sample_expression_loop(camera_index=0, interval=1.25):
    global _running

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("❌ Unable to access camera for expression tracking.")
        return

    print("🎭 Expression tracking started...")

    while _running:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to capture frame.")
            continue

        try:
            result = _detector.top_emotion(frame)
            if result:
                emotion, confidence = result
                _expression_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "expression": emotion,
                    "confidence": confidence
                })
                
                if emotion is not None and confidence is not None:
                    print(f"🧠 Logged expression: {emotion} ({confidence:.2f})")
                else:
                    print("🧠 Detected a face, but expression is unclear.")
        except Exception as e:
            print(f"❌ FER error: {e}")

        time.sleep(interval)

    cap.release()
    print("🛑 Expression tracking stopped.")

# ✅ Start tracking
def start_tracking():
    global _running, _thread
    if _running:
        return
    _running = True
    _thread = threading.Thread(target=_sample_expression_loop, daemon=True)
    _thread.start()

# ❌ Stop tracking (e.g. at end of sim)
def stop_tracking():
    global _running
    _running = False
    if _thread:
        _thread.join()

# 🔍 For preceptor to use
def get_expression_log():
    return _expression_log.copy()

# Optional: reset log between runs
def clear_log():
    global _expression_log
    _expression_log = []

if __name__ == "__main__":
    start_tracking()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_tracking()
        print("📊 Final Log:", get_expression_log())
