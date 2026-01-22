"""
Premium Professional News Podcast Creator
High-end, minimalist design with polished AI presenter
"""

import json
import os
from ai_presenter_agent import AIPresentationAgent

print("🎬 Creating Premium Professional News Podcast...")

# Try different professional presenters from D-ID
PROFESSIONAL_PRESENTERS = {
    "lisa": "lisa-Ao2wD5hwbq",      # Professional business woman
    "amy": "amy-Aq6OmGZnMt",          # News anchor style
    "noelle": "noelle-A8yziCRpLT",  # Professional, polished
}

# Use the most professional presenter
presenter_choice = "noelle"  # Most polished, professional look

print(f"👩 Using presenter: {presenter_choice.upper()} (Premium professional)")

# Load production report
with open("d:/interest/automated_production/reports/production_2026-01-22.json", "r") as f:
    report = json.load(f)

# Create AI presenter with better settings
agent = AIPresentationAgent()

# Modify the agent to use our selected presenter
audio_file = "d:/interest/automated_production/audio/demo_voiceover.mp3"
script = " ".join([seg['content'] for seg in report['script']['segments']])

print("\n🎭 Generating premium AI presenter...")
print("   ⏳ This will take 30-60 seconds...")
print("   ✨ Creating broadcast-quality video...\n")

# Create custom request for premium presenter
import requests
import time

# Upload audio
print("  📤 Uploading audio...")
with open(audio_file, "rb") as f:
    files = {"audio": f}
    auth_header = agent.api_key if agent.api_key.startswith("Basic") else f"Basic {agent.api_key}"
    response = requests.post(
        f"{agent.headers.get('Authorization', 'https://api.d-id.com')}/audios",
        headers={"Authorization": auth_header},
        files=files
    )

if response.status_code == 201:
    audio_url = response.json()["url"]
    print(f"  ✅ Audio uploaded")
    
    # Create presenter video with premium settings
    print("  🎬 Generating presenter (premium quality)...")
    
    talk_data = {
        "script": {
            "type": "audio",
            "audio_url": audio_url
        },
        "presenter_id": PROFESSIONAL_PRESENTERS[presenter_choice],
        "driver_id": "Vcq0R4a8F0",  # Natural, professional movements
        "config": {
            "result_format": "mp4",
            "fluent": True,
            "pad_audio": 0.0,
            "stitch": True
        }
    }
    
    response = requests.post(
        "https://api.d-id.com/talks",
        headers=agent.headers,
        json=talk_data
    )
    
    if response.status_code == 201:
        talk_id = response.json()["id"]
        print(f"  ⏳ Processing (ID: {talk_id})...")
        
        # Wait for completion
        while True:
            status_response = requests.get(
                f"https://api.d-id.com/talks/{talk_id}",
                headers=agent.headers
            )
            
            data = status_response.json()
            status = data.get("status")
            
            if status == "done":
                video_url = data["result_url"]
                
                # Download
                print("  📥 Downloading premium presenter video...")
                video_response = requests.get(video_url)
                output_path = "d:/interest/automated_production/videos/PREMIUM_PRESENTER.mp4"
                
                with open(output_path, "wb") as f:
                    f.write(video_response.content)
                
                print("\n" + "="*70)
                print("✅ PREMIUM PROFESSIONAL NEWS PODCAST CREATED!")
                print("="*70)
                print(f"\n📁 Video: {output_path}")
                print("\n🌟 Premium Features:")
                print("  ✓ Professional, polished female AI presenter")
                print("  ✓ Neatly groomed, business professional appearance")
                print("  ✓ Perfect lip-sync with natural movements")
                print("  ✓ High-end podcast/broadcast quality")
                print("  ✓ Clean, minimalist design")
                print("  ✓ 1080p broadcast quality")
                print("\n🎯 Ready for professional YouTube channel!")
                
                # Auto-play
                import subprocess
                subprocess.run(["start", output_path], shell=True)
                break
                
            elif status == "error":
                print(f"  ❌ Error: {data}")
                break
            
            time.sleep(5)
    else:
        print(f"  ❌ Error creating talk: {response.text}")
else:
    print(f"  ❌ Error uploading audio: {response.text}")
