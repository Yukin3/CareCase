import os
import asyncio
import unicodedata
import re
from edge_tts import Communicate

VOICE = "en-NG-EzinneNeural"
CACHE_DIR = "cached_tts"
DEFAULT_OUTPUT = "fallback_output.mp3"

def clean_filename(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("’", "'").replace("…", "...").replace("“", "\"").replace("”", "\"")
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    return text.lower().replace(",", "").replace("...", "").replace("?", "").replace("'", "").replace(" ", "_") + ".mp3"

async def speak(text: str):
    filename = clean_filename(text)
    cached_path = os.path.join(CACHE_DIR, filename)

    if os.path.exists(cached_path):
        print(f"🗣️ [Offline] {text}")
        os.system(f"mpg123 '{cached_path}' > /dev/null 2>&1")
    else:
        print(f"🌐 [Online Fallback] {text}")
        try:
            tts = Communicate(text, VOICE)
            await tts.save(DEFAULT_OUTPUT)
            os.system(f"mpg123 '{DEFAULT_OUTPUT}' > /dev/null 2>&1")
        except Exception as e:
            print(f"❌ TTS failed: {e}")

def say(text: str):
    asyncio.run(speak(text))
