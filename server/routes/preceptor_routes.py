from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import os
import json
import glob
from dotenv import load_dotenv
from services.preceptor import fetch_interaction_log, score_interaction_with_gpt, score_interaction_offline
from utils.score_utils import score_interaction_offline, score_gaze_log

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["CareCase"]
collection = db["interaction_logs"]


router = APIRouter()

class Turn(BaseModel):
    ai_line: str
    user_input: str
    timestamp: float
    emotion: str = "neutral"

class InteractionLog(BaseModel):
    scenario_id: str
    role: str
    session_id: str
    start_time: float
    turns: List[Turn]


def find_gaze_log(session_id):
    pattern = os.path.join("data", "gaze_logs", f"{session_id}*.json")
    files = glob.glob(pattern)
    return files[0] if files else None


@router.get("/score/{session_id}")
def score_session(session_id: str, online: bool = True):
    log = fetch_interaction_log(session_id)
    if not log:
        return {"error": "Session log not found"}
    
    # 🧠 Score interaction
    if online:
        raw_feedback = score_interaction_with_gpt(log)
        try:
            interaction_score = json.loads(raw_feedback) if isinstance(raw_feedback, str) else raw_feedback
        except Exception as e:
            print(f"❌ Failed to parse GPT feedback: {e}")
            interaction_score = {"score": 0, "feedback": "[Scoring unavailable]", "per_turn_feedback": []}
    else:
        script_lines = next(
            (s["script"] for s in SCRIPT_DB if s["scenario_id"] == log["scenario_id"] and s["role"] == log["role"]),
            []
        )
        interaction_score = score_interaction_offline(log, expected_script_lines=script_lines)


    # 👁️ Score gaze
    gaze_path = find_gaze_log(session_id)
    if gaze_path:
        with open(gaze_path, "r", encoding="utf-8") as f:
            gaze_log = json.load(f)
        gaze_score = score_gaze_log(gaze_log)
    else:
        print(f"⚠️ Gaze log not found for {session_id}")
        gaze_score = {"gaze_score": 0.0, "feedback": "[Gaze data unavailable]"}


    # 🎯 Combine
    interaction_value = interaction_score.get("score", 0) if isinstance(interaction_score, dict) else 0
    gaze_value = gaze_score.get("gaze_score", 0) if isinstance(gaze_score, dict) else 0
    final_score = round((interaction_value + gaze_value) / 2, 2)



    return {
        "session_id": session_id,
        "score": final_score,
        "interaction": interaction_score,
        "gaze": gaze_score
    }



with open(os.path.join(os.path.dirname(__file__), "..", "data", "scenario_scripts.json"), "r", encoding="utf-8") as f:
    SCRIPT_DB = json.load(f)

@router.post("/score")
def score_and_store(log: InteractionLog, online: bool = True):
    log_dict = log.dict()

    try:     # Save log (online)
        collection.insert_one(log_dict)
    except Exception as e: # Skip if offline
        print(f"⚠️ MongoDB save failed: {e}")

    # 🧠 Interaction scoring
    if online:    # Score with GPT
        raw_feedback = score_interaction_with_gpt(log_dict)
        try:
            interaction_score = json.loads(raw_feedback) if isinstance(raw_feedback, str) else raw_feedback
        except Exception as e:
            print(f"❌ Failed to parse GPT feedback: {e}")
            interaction_score = {
                "score": 0,
                "feedback": "[Scoring unavailable]",
                "per_turn_feedback": []
            }
    else: # Compare w/ offline script
        script_lines = next(
            (s["script"] for s in SCRIPT_DB if s["scenario_id"] == log_dict["scenario_id"] and s["role"] == log_dict["role"]),
            []
        )
        interaction_score = score_interaction_offline(log_dict, expected_script_lines=script_lines)


    # 👁️ Gaze scoring
    session_id = log_dict["session_id"]
    gaze_path = find_gaze_log(session_id)
    if gaze_path:
        with open(gaze_path, "r", encoding="utf-8") as f:
            gaze_log = json.load(f)
        gaze_score = score_gaze_log(gaze_log)
    else:
        print(f"⚠️ Gaze log not found for {session_id}")
        gaze_score = {"gaze_score": 0.0, "feedback": "[Gaze data unavailable]"}

    # 🎯 Final score
    interaction_value = interaction_score.get("score", 0)
    gaze_value = gaze_score.get("gaze_score", 0)
    final_score = round((interaction_value + gaze_value)/2, 2)


    return {
        "message": "Log saved and scored",
        "session_id": session_id,
        "score": final_score,
        "interaction": interaction_score,
        "gaze": gaze_score
    }