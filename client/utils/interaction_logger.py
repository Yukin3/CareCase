import time
import json
import uuid
import os

class InteractionLogger:
    def __init__(self, scenario_id, role="patient", logs_dir="data/interaction_logs"):
        self.session_id = f"{scenario_id}_{uuid.uuid4().hex[:6]}"
        self.log = {
            "scenario_id": scenario_id,
            "role": role,
            "session_id": self.session_id,
            "start_time": time.time(),
            "turns": []
        }
        self.logs_dir = logs_dir
        os.makedirs(logs_dir, exist_ok=True)

    def log_turn(self, ai_line, user_input, emotion=None):
        self.log["turns"].append({
            "ai_line": ai_line,
            "user_input": user_input,
            "timestamp": time.time(),
            "emotion": emotion or "neutral"
        })

    def save_to_file(self):
        path = os.path.join(self.logs_dir, f"{self.session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.log, f, indent=2)
        return path

    def get_log(self):
        return self.log
