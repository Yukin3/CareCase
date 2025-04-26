import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.listener import listen_and_transcribe
from services.responder import generate_clinical_response
from services.speaker import say
from services.expressions import start_tracking, stop_tracking, get_expression_log, clear_log
import json
import time

# 🔹 Load scenario from file or define inline for now
with open("data/scenario_scripts.json", "r") as f:
    scenarios = json.load(f)

scenario = scenarios[0]  # default to first scenario
script_intro = scenario["script"][0]["text"]  # First patient line

print("🧠 Scenario loaded:", scenario["title"])
print("📍 Context:", scenario["description"])
print("🧵 Starting interaction...\n")
clear_log()
start_tracking()


# 👂 Speak first line
say(script_intro)
last_line = script_intro

while True:
    print("\n🎤 Your turn to speak:")
    student_input = listen_and_transcribe()

    print(f"🧑‍⚕️ You said: {student_input}")

    if student_input.lower() in ["exit", "quit", "q"]:
        print("🛑 Ending simulation.")
        break

    # 🤖 Generate AI response
    response = generate_clinical_response(
        scenario=scenario,
        last_line=last_line,
        user_input=student_input,
        role="patient"  # or "nurse", "doctor", etc
    )

    print(f"🤖 {scenario['role'].capitalize()} says: {response}")
    say(response)

    last_line = response
    time.sleep(0.5)

stop_tracking()
log = get_expression_log()
print("📊 Final Expression Log:", log)