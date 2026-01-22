import json
from gtts import gTTS
import os

# Load the latest production report
with open("d:/interest/automated_production/reports/production_2026-01-22.json", "r") as f:
    report = json.load(f)

# Extract script content
script_segments = report['script']['segments']
full_text = " ".join([seg['content'] for seg in script_segments])

# Generate audio using Google TTS
print("Generating voice-over using Google Text-to-Speech...")
tts = gTTS(text=full_text, lang='en', slow=False)
audio_path = "d:/interest/automated_production/audio/demo_voiceover.mp3"
tts.save(audio_path)
print(f"Audio generated: {audio_path}")

# Now re-run video assembly with this audio
print("\nNow run: python automated_intelligence_pipeline.py to regenerate video with audio")
