import os
import subprocess
import uuid

WHISPER_PATH = "/home/Yukin3/tools/whisper.cpp/build/bin/whisper-cli"
MODEL_PATH = "/home/Yukin3/tools/whisper.cpp/models/ggml-base.en.bin"
AUDIO_DEVICE = "plughw:2,0"  # QuadCast input
AUDIO_FILENAME = f"temp_{uuid.uuid4().hex[:8]}.wav"

def listen_and_transcribe(duration=5):
    print("🎙️ Listening from mic...")

    # Record audio
    arecord_cmd = [
        "arecord",
        "-D", AUDIO_DEVICE,
        "-f", "S16_LE", #16-bit PCM audio
        "-t", "wav", # File output
        "-c", "1", # Mono
        "-d", str(duration), 
        "-r", "16000", # Sample rate
        AUDIO_FILENAME
    ]

    subprocess.run(arecord_cmd, check=True)
    print("🎧 Recorded. Transcribing...")

    try:
        whisper_cmd = [
            WHISPER_PATH,
            "-m", MODEL_PATH,
            "-f", AUDIO_FILENAME,
            "-nt"
        ]
        result = subprocess.run(whisper_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        #Debugging
        print("----- Whisper Output -----")
        print(output)

        # Clean up audio file
        # os.remove(AUDIO_FILENAME) #TODO: Uncomment to prevnt file saves

        # Extract transcript from output
        lines = output.strip().split("\n")
        clean_lines = [line.strip() for line in lines if line.strip()]
        if clean_lines:
            return clean_lines[-1]
        else:
            return "[no speech detected]"

    except subprocess.CalledProcessError as e:
        print("❌ Whisper failed:", e.stderr)
        return None
    
if __name__ == "__main__":
    transcript = listen_and_transcribe()
    print(f"📝 Transcript: {transcript}")
