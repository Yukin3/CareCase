import os
import json
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global script tracking for offline use
SCRIPT_INDEX = {}

# Load scripts once when the module is loaded
with open(os.path.join(os.path.dirname(__file__), "..", "data", "scenario_scripts.json"), "r", encoding="utf-8") as f:
    SCRIPT_DB = json.load(f)

def generate_clinical_response(scenario, last_line=None, user_input=None, role="patient", language="en-US", online=True, script=None):
    role_instruction = {
        "patient": "You are playing the role of a culturally diverse patient in a medical simulation.",
        "doctor": "You are simulating a thoughtful, professional doctor conducting an interview or exam.",
        "nurse": "You are a nurse engaging in patient triage or bedside support in a clinical setting."
    }.get(role, "You are participating in a clinical simulation.")

    # --- OFFLINE MODE ---
    if not online:
        scenario_id = scenario["id"]

        # Find matching script
        script = next((s for s in SCRIPT_DB if s["scenario_id"] == scenario["id"] and s["role"] == role), None)
        if not script:
            return "[No script found for this scenario and role]"

        if scenario_id not in SCRIPT_INDEX:
            SCRIPT_INDEX[scenario_id] = 0

        idx = SCRIPT_INDEX[scenario_id]
        lines = script.get("script", [])

        if idx < len(lines):
            SCRIPT_INDEX[scenario_id] += 1
            return lines[idx]["text"]
        else:
            return "[End of scripted lines]"

    # --- ONLINE MODE ---
    scenario_context = f"""Scenario Context:
- Title: {scenario['title']}
- Description: {scenario['description']}
- Category: {scenario.get('category', '')}
- Time: {scenario.get('time_of_day', '')}
- Location: {scenario.get('location', {}).get('name', 'unknown')}
- Environment: {scenario.get('environmental_context', '')}
- Symptoms: {', '.join(scenario.get('symptoms', []))}
"""

    if not last_line:
        # First line (cold open)
        user_prompt = f"""
{scenario_context}
Start the interaction as a {role} in a natural and realistic way.
Use the scenario info above, including emotion, culture, or setting cues.
Respond in {language}. Keep it concise.
"""
    else:
        # Follow-up
        user_prompt = f"""
{scenario_context}
Last line in the interaction:
\"{last_line}\"

The user just said:
\"{user_input}\"

Reply as the {role}, continuing the interaction naturally.
Respond in {language}.
"""

    messages = [
        {"role": "system", "content": role_instruction},
        {"role": "user", "content": user_prompt.strip()}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=120
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT failed: {e}")
        return "[AI unavailable]"
