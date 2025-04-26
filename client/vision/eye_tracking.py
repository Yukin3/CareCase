import time
import json
import os
import uuid

class GazeLogger:
    def __init__(self, session_id, logs_dir="data/gaze_logs"):
        self.session_id = session_id or f"unknown_{uuid.uuid4().hex[:6]}"
        self.log = {
            "session_id": self.session_id,
            "start_time": time.time(),
            "samples": []  # each sample will include timestamp, eye_contact, and direction
        }
        self.logs_dir = logs_dir
        os.makedirs(logs_dir, exist_ok=True)

    def log_sample(self, eye_contact, gaze_direction, left_iris=None, right_iris=None):
        sample = {
            "timestamp": time.time(),
            "eye_contact": eye_contact,
            "gaze_direction": gaze_direction
        }
        if left_iris and right_iris:
            sample["left_iris"] = left_iris
            sample["right_iris"] = right_iris
        self.log["samples"].append(sample)
        

    def save_to_file(self):
        path = os.path.join(self.logs_dir, f"{self.session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.log, f, indent=2)
        return path

    def get_log(self):
        return self.log
