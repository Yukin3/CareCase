import openai
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from utils.score_utils import score_interaction_offline

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["CareCase"]
collection = db["interaction_logs"]

def fetch_interaction_log(session_id):
    return collection.find_one({"session_id": session_id})

def score_interaction_with_gpt(log):
    turns = log.get("turns", [])
    role = log.get("role", "patient")

    conversation_text = "\n".join(
        [f"AI: {t['ai_line']}\nUser: {t['user_input']}" for t in turns]
    )

    prompt = f"""
You are a clinical evaluator scoring a simulation where a student (user) interviews a {role} (AI-generated).
Each turn includes what the patient said and how the student responded.
Please score how well the student responded in each turn, using a scale of 0 to 3.

Give higher scores to responses that are:
- clear and concise
- medically relevant
- empathetic and appropriate to the patient's needs

Give lower scores if the student:
- gives vague or generic replies
- shows a lack of empathy or clinical understanding
- gives long or confusing answers that don't match the patient's concern

The total score should be the sum of all per-turn scores, scaled to 10 using:
(score_sum / (3 × total_turns)) × 10

Your response MUST be returned in this exact JSON format:

{{
  "score": float (total score out of 10),
  "feedback": str (overall summary),
  "per_turn_feedback": [
    {{
      "turn": int,
      "student_reply": str,
      "score": int (0–3),
      "comment": str
    }},
    ...
  ]
}}

Session Context:
- Scenario ID: {log['scenario_id']}
- Total Turns: {len(turns)}

Interaction:
"""

    for i, t in enumerate(turns):
        prompt += f"\nTurn {i+1}:"
        prompt += f"\n  Patient said: \"{t['ai_line']}\""
        prompt += f"\n  Student replied: \"{t['user_input']}\"\n"

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical simulation evaluator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT scoring failed:", e)
        return "[Scoring unavailable]"

