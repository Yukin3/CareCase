import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "server")))

from services.speaker import say  # your async edge-tts wrapper
from services.listener import listen_and_transcribe
from services.responder import generate_clinical_response
from utils.interaction_logger import InteractionLogger

# Global memory (optional — could be stateful if needed later)
last_line = None

def run_audio_interaction_line(
    scenario, role="patient", language="en-US", update_caption_callback=None, online=True, logger=None
) -> str:
    global last_line

     # 1. Generate next line using GPT or fallback
    print("🧠 Generating AI line...")
    try:
        line_text = generate_clinical_response(
            scenario=scenario,
            last_line=last_line,
            user_input=None,  # No user input yet at this point
            role=role,
            language=language,
            online=online
        )
    except Exception as e:
        print("❌ GPT Error:", e)
        line_text = "[Could not generate response]"


    # 2. Show line in captions and speak it
    if update_caption_callback:
        update_caption_callback(line_text)

    print(f"🗣️ Speaking: {line_text}")
    say(line_text)

    # 3. Listen for user input (simulated conversation turn)
    print("🎙️ Listening...")
    user_response = listen_and_transcribe()
    print(f"📝 Transcribed: {user_response}")

    # 4. Save this AI line as last_line for context in next loop
    last_line = line_text

    # 5. Log the turn if logger is provided
    if logger:
        logger.log_turn(ai_line=line_text, user_input=user_response)


    # 4. Save this AI line as last_line for context in next loop
    last_line = line_text

    return user_response
