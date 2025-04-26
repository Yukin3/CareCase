import os
import json
import asyncio
import unicodedata
import re
from edge_tts import Communicate

VOICE = "en-NG-EzinneNeural"
OUTPUT_DIR = "cached_tts"

SCENARIO_PATH = "data/scenario_scripts.json"

def filename_from_text(text):
    return text.lower().replace(",", "").replace("...", "").replace("?", "").replace("'", "").replace(" ", "_") + ".mp3"

def clean_text(text):
    # Normalize unicode and remove problematic characters
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("’", "'").replace("…", "...")  # common replacements
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # remove any remaining non-ASCII
    return text

async def generate_from_script():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(SCENARIO_PATH, "r") as f:
        scenarios = json.load(f)

    all_lines = []
    for scenario in scenarios:
        for line in scenario.get("script", []):
            all_lines.append(line["text"])

    for text in all_lines:
        filename = filename_from_text(text)
        path = os.path.join(OUTPUT_DIR, filename)

        if not os.path.exists(path):
            print(f"Generating: {text}")
            tts = Communicate(clean_text(text), VOICE)
            try:
                await tts.save(path)
                await asyncio.sleep(1)  
            except Exception as e:
                print(f"❌ Failed for: {text}\n{e}")
        else:
            print(f"Already cached..: {text}")

asyncio.run(generate_from_script())
