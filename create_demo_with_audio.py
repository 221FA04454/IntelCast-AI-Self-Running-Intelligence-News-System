import json
import os
import requests

# Load the production report
with open("d:/interest/automated_production/reports/production_2026-01-22.json", "r") as f:
    report = json.load(f)

# Import the VideoAssemblyAgent
import sys
sys.path.append("d:/interest")
from automated_intelligence_pipeline import VideoAssemblyAgent, OUTPUT_DIR

# Create demo video with new audio
agent = VideoAssemblyAgent()
audio_path = "d:/interest/automated_production/audio/demo_voiceover.mp3"
video_assets = report['video_assets']

print("Creating demo video with AI voice narration...")
final_video = agent.assemble(audio_path, video_assets)

if final_video:
    print(f"\n✅ Demo video created successfully!")
    print(f"📁 Location: {final_video}")
    print(f"\nThis video includes:")
    print("  - 5 news stories with relevant stock footage")
    print("  - AI voice narration explaining each story")
    print("  - Professional transitions and formatting")
else:
    print("❌ Video generation failed. Check logs for details.")
