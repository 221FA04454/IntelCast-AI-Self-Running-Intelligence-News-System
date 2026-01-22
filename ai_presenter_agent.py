"""
D-ID AI Presenter Integration for News Pipeline
Creates realistic AI talking head videos with lip-sync
"""

import requests
import json
import time
import os

# D-ID API Configuration
D_ID_API_KEY = "c3VtYW50aG9mZmljaWFsMjYyNkBnbWFpbC5jb20:GCQQcSPtWXMr9YnIvjb4E"  # Get from https://studio.d-id.com/
D_ID_API_URL = "https://api.d-id.com"

class AIPresentationAgent:
    """Creates realistic AI news presenter videos using D-ID"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or D_ID_API_KEY
        self.headers = {
            "Authorization": self.api_key if self.api_key.startswith("Basic") else f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_presenter_video(self, audio_path, script_text, presenter_image=None):
        """
        Create AI presenter video with lip-sync
        
        Args:
            audio_path: Path to audio file (.mp3)
            script_text: Text being spoken (for better lip-sync)
            presenter_image: Optional custom presenter image URL
            
        Returns:
            Path to generated presenter video
        """
        print("🎬 Creating AI presenter video with D-ID...")
        
        # Use D-ID's built-in presenter (Amy - professional female)
        # Available presenters: https://docs.d-id.com/reference/presenters
        presenter_id = "amy-Aq6OmGZnMt"  # Professional female presenter
        
        # Upload audio to D-ID
        print("  ⬆️  Uploading audio...")
        audio_url = self._upload_audio(audio_path)
        
        # Create talking photo request using text-to-speech
        print("  🎭 Generating presenter...")
        talk_data = {
            "script": {
                "type": "audio",
                "audio_url": audio_url
            },
            "presenter_id": presenter_id,
            "driver_id": "Vcq0R4a8F0"
        }
        
        response = requests.post(
            f"{D_ID_API_URL}/talks",
            headers=self.headers,
            json=talk_data
        )
        
        if response.status_code != 201:
            raise Exception(f"D-ID API Error: {response.text}")
        
        talk_id = response.json()["id"]
        print(f"  ⏳ Processing (ID: {talk_id})...")
        
        # Wait for video generation
        video_url = self._wait_for_completion(talk_id)
        
        # Download generated video
        output_path = f"d:/interest/automated_production/videos/ai_presenter_{int(time.time())}.mp4"
        print(f"  ⬇️  Downloading presenter video...")
        
        video_response = requests.get(video_url)
        with open(output_path, "wb") as f:
            f.write(video_response.content)
        
        print(f"  ✅ AI presenter video created: {output_path}")
        return output_path
    
    def _upload_audio(self, audio_path):
        """Upload audio file to D-ID and return URL"""
        auth_header = self.api_key if self.api_key.startswith("Basic") else f"Basic {self.api_key}"
        with open(audio_path, "rb") as f:
            files = {"audio": f}
            response = requests.post(
                f"{D_ID_API_URL}/audios",
                headers={"Authorization": auth_header},
                files=files
            )
        
        if response.status_code != 201:
            raise Exception(f"Audio upload failed: {response.text}")
        
        return response.json()["url"]
    
    def _wait_for_completion(self, talk_id, max_wait=300):
        """Wait for D-ID to finish generating video"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = requests.get(
                f"{D_ID_API_URL}/talks/{talk_id}",
                headers=self.headers
            )
            
            data = response.json()
            status = data.get("status")
            
            if status == "done":
                return data["result_url"]
            elif status == "error":
                raise Exception(f"D-ID generation failed: {data}")
            
            time.sleep(5)
        
        raise Exception("Timeout waiting for D-ID video generation")


# Demo usage
if __name__ == "__main__":
    # Test with existing audio
    agent = AIPresentationAgent()
    
    audio_file = "d:/interest/automated_production/audio/demo_voiceover.mp3"
    script = "Global alert for January 22, 2026. Major shifts in geopolitics..."
    
    try:
        presenter_video = agent.create_presenter_video(audio_file, script)
        print(f"\n✅ Success! Presenter video: {presenter_video}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📝 To use D-ID:")
        print("1. Sign up at https://studio.d-id.com/")
        print("2. Get your API key from Settings > API")
        print("3. Update D_ID_API_KEY in this file")
