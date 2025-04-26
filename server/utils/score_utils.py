from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util
from collections import Counter

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


# Load once at module level
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def compute_similarity(user_input, expected_line):
    if not user_input.strip() or not expected_line.strip():
        return 0.0

    embeddings = model.encode([user_input, expected_line], convert_to_tensor=True)
    sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return round(float(sim), 2)


def score_interaction_offline(log, expected_script_lines):
    from math import floor
    turns = log.get("turns", [])
    feedback = []
    total = 0

    for i, turn in enumerate(turns):
        user_text = turn["user_input"]
        expected = expected_script_lines[i]["text"] if i < len(expected_script_lines) else ""

        similarity = compute_similarity(user_text, expected)
        scaled_score = max(0.0, round(similarity * 3, 2))  # scale from 0 to 3

        feedback.append({
            "turn": i + 1,
            "student_reply": user_text,
            "expected_line": expected,
            "score": scaled_score,
            "comment": "Auto-scored using similarity. Higher score = closer match to expected."
        })

        total += scaled_score

    out_of = len(turns) * 3
    return {
        "score": round(total, 2),
        "feedback": f"Offline similarity-based score for {len(turns)} turns.",
        "per_turn_feedback": feedback
    }



def score_gaze_log(gaze_log):
    samples = gaze_log.get("samples", [])
    if not samples:
        return {
            "gaze_score": 0.0,
            "eye_contact_percentage": 0.0,
            "dominant_direction": "unknown",
            "total_samples": 0,
            "feedback": "No gaze data available."
        }

    total = len(samples)
    eye_contact_count = sum(1 for s in samples if s["eye_contact"])
    directions = [s["gaze_direction"] for s in samples]

    # 💡 Basic metrics
    eye_contact_ratio = eye_contact_count / total
    direction_counts = Counter(directions)
    dominant_direction = direction_counts.most_common(1)[0][0]

    # 🎯 Scoring logic (scale to 10)
    # You can refine this with more nuance later
    contact_score = eye_contact_ratio * 10
    attention_bonus = 2 if dominant_direction == "center" else 0
    final_score = round(min(contact_score + attention_bonus, 10), 2)

    # 📢 Feedback summary
    feedback = (
        f"Maintained eye contact {round(eye_contact_ratio * 100)}% of the time.\n"
        f"Most common gaze direction: {dominant_direction}.\n"
        "Bonus points awarded for staying centered." if dominant_direction == "center" else
        "Consider looking more toward the subject to improve perceived attentiveness."
    )

    return {
        "gaze_score": final_score,
        "eye_contact_percentage": round(eye_contact_ratio * 100, 2),
        "dominant_direction": dominant_direction,
        "total_samples": total,
        "feedback": feedback
    }
