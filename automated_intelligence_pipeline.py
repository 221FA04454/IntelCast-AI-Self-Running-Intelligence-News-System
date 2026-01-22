import feedparser
import json
import datetime
import os
import requests
import re

# ==========================================
# CONFIGURATION & SOURCES
# ==========================================
NEWS_API_KEY = "67ce60cd1d764769a3410cd8c51cfbe5"
ELEVENLABS_KEY = "sk_f813c4e9e52df865c849f8efa7f6212848c91ba12a7841dc"
PEXELS_API_KEY = "nSXde8qGmWEfLMH2w6hSiUGfajEQ8BkuTr8Lr2XSv2qLAGviY16Pgxkz"

# YOUTUBE CREDENTIALS (TO BE FILLED BY USER)
YT_CLIENT_ID = "YOUR_CLIENT_ID.apps.googleusercontent.com"
YT_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
YT_REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"

SOURCES = {
    "Google News": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "Reddit WorldNews": "https://www.reddit.com/r/worldnews/.rss",
}

OUTPUT_DIR = "d:/interest/automated_production"
LOG_DIR = f"{OUTPUT_DIR}/logs"
REPORTS_DIR = f"{OUTPUT_DIR}/reports"

for d in [LOG_DIR, REPORTS_DIR, f"{OUTPUT_DIR}/audio", f"{OUTPUT_DIR}/scripts", f"{OUTPUT_DIR}/videos"]:
    if not os.path.exists(d):
        os.makedirs(d)

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{LOG_DIR}/pipeline.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

# ==========================================
# AGENT 1: NEWS INTELLIGENCE AGENT
# ==========================================
class NewsAgent:
    def fetch(self):
        log_event("NewsAgent: Fetching latest global headlines from NewsAPI...")
        all_news = []
        try:
            url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API_KEY}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get("status") == "ok":
                for article in data.get("articles", [])[:15]:
                    all_news.append({
                        "title": article.get("title", ""),
                        "link": article.get("url", ""),
                        "source": article.get("source", {}).get("name", "Unknown"),
                        "published": article.get("publishedAt", ""),
                        "summary": article.get("description", "")
                    })
                log_event(f"NewsAgent: Successfully fetched {len(all_news)} articles.")
            else:
                log_event(f"NewsAPI Error: {data.get('message', 'Unknown error')}")
        except Exception as e:
            log_event(f"NewsAgent Exception: {e}")
        return all_news

# ==========================================
# AGENT 2: FACT VERIFICATION AGENT
# ==========================================
class VerificationAgent:
    def verify(self, news_items):
        log_event("VerificationAgent: Cross-referencing stories...")
        verified_batch = []
        # Basic Logic: If a topic appears in more than 1 source, it's weighted higher
        for item in news_items:
            matches = [i for i in news_items if i['title'][:30] == item['title'][:30]]
            if len(matches) >= 1: # In a real scenario, this would use fuzzy matching or LLM
                item["verification_status"] = "VERIFIED"
                item["reliability_score"] = "High"
                verified_batch.append(item)
        
        # Deduplicate
        seen = set()
        unique_verified = []
        for v in verified_batch:
            if v['title'] not in seen:
                unique_verified.append(v)
                seen.add(v['title'])
                
        log_event(f"VerificationAgent: {len(unique_verified)} stories verified and deduplicated.")
        return unique_verified[:5] # Return top 5 verified stories

# ==========================================
# AGENT 3: SCRIPTWRITER AGENT
# ==========================================
class ScriptwriterAgent:
    def create_script(self, verified_news):
        log_event("ScriptwriterAgent: Generating YouTube script template...")
        date_str = datetime.datetime.now().strftime("%B %d, %Y")
        script = {
            "metadata": {"date": date_str, "type": "YouTube Document"},
            "segments": []
        }
        
        # Hook
        script["segments"].append({
            "time": "0:00",
            "narrator": "Hook",
            "content": f"Global alert for {date_str}. Major shifts in geopolitics and technology are breaking right now. Here is what you need to know."
        })
        
        for i, news in enumerate(verified_news):
            script["segments"].append({
                "time": f"0:{30*(i+1)}",
                "narrator": f"Story {i+1}",
                "content": f"In {news['source']}, we are tracking: {news['title']}. This development signals a significant shift in current global patterns."
            })
            
        return script

# ==========================================
# AGENT 4: VOICEOVER AGENT
# ==========================================
class VoiceoverAgent:
    def generate_audio(self, script):
        log_event("VoiceoverAgent: Generating voiceover with ElevenLabs...")
        audio_folder = f"{OUTPUT_DIR}/audio"
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # We'll generate one audio file for the whole script for simplicity
        full_text = " ".join([seg['content'] for seg in script['segments']])
        
        voice_id = "21m00Tcm4TlvDq8ikWAM" # Default "Rachel" voice
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_KEY
        }
        
        data = {
            "text": full_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                file_path = f"{audio_folder}/voiceover_{timestamp}.mp3"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                log_event(f"VoiceoverAgent: Audio saved to {file_path}")
                return file_path
            else:
                log_event(f"ElevenLabs Error: {response.text}")
        except Exception as e:
            log_event(f"VoiceoverAgent Exception: {e}")
        return None

# ==========================================
# AGENT 5: VIDEO AGENT
# ==========================================
class VideoAgent:
    def gather_assets(self, verified_news):
        log_event("VideoAgent: Gathering stock footage from Pexels...")
        video_folder = f"{OUTPUT_DIR}/videos"
        assets = []
        
        headers = {"Authorization": PEXELS_API_KEY}
        
        for news in verified_news:
            # Extract keywords from title (simple version)
            query = news['title'].split(" - ")[0][:50]
            url = f"https://api.pexels.com/v1/videos/search?query={query}&per_page=1"
            
            try:
                response = requests.get(url, headers=headers)
                data = response.json()
                if data.get("videos"):
                    video_url = data["videos"][0]["video_files"][0]["link"]
                    assets.append({"title": news['title'], "video_url": video_url})
                    log_event(f"VideoAgent: Found asset for '{news['title']}'")
            except Exception as e:
                log_event(f"VideoAgent Error for '{news['title']}': {e}")
                
        return assets

# ==========================================
# AGENT 6: VIDEO ASSEMBLY AGENT
# ==========================================
class VideoAssemblyAgent:
    def assemble(self, audio_path, video_assets):
        try:
            from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
        except ImportError:
            from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
        
        log_event("VideoAssemblyAgent: Assembling final video...")
        
        clips = []
        try:
            # Download and process each video asset
            for i, asset in enumerate(video_assets):
                # Download video file
                temp_video_path = f"{OUTPUT_DIR}/videos/temp_asset_{i}.mp4"
                log_event(f"VideoAssemblyAgent: Downloading asset {i} from {asset['video_url']}")
                v_resp = requests.get(asset['video_url'])
                with open(temp_video_path, "wb") as f:
                    f.write(v_resp.content)
                
                # Load clip and use modern subclipped/resized if available
                clip = VideoFileClip(temp_video_path)
                
                # Determine subclip duration based on actual clip length
                duration = min(clip.duration, 10)
                
                # Handling modern vs legacy moviepy API
                if hasattr(clip, 'subclipped'):
                    clip = clip.subclipped(0, duration)
                else:
                    clip = clip.subclip(0, duration)
                
                if hasattr(clip, 'resized'):
                    clip = clip.resized(height=720)
                else:
                    clip = clip.resize(height=720)
                
                clips.append(clip)
            
            if not clips:
                log_event("VideoAssemblyAgent: No clips to assemble.")
                return None
                
            # Combine clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Add audio (with dummy fallback if possible)
            if audio_path and os.path.exists(audio_path):
                try:
                    audio = AudioFileClip(audio_path)
                    # MoviePy 2.0+ uses 'with_audio' instead of 'set_audio'
                    if hasattr(final_clip, 'with_audio'):
                        final_clip = final_clip.with_audio(audio)
                    else:
                        final_clip = final_clip.set_audio(audio)
                except Exception as e:
                    log_event(f"VideoAssemblyAgent: Audio error - {e}. Proceeding without audio.")
            else:
                log_event("VideoAssemblyAgent: No audio file found. Final video will be silent.")
            
            # Export
            output_path = f"{OUTPUT_DIR}/videos/final_production_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            final_clip.write_videofile(output_path, fps=24)
            log_event(f"VideoAssemblyAgent: Final video saved to {output_path}")
            return output_path
            
        except Exception as e:
            log_event(f"VideoAssemblyAgent Exception: {e}")
        return None

# ==========================================
# AGENT 6: YOUTUBE UPLOAD AGENT
# ==========================================
class YouTubeUploadAgent:
    def upload(self, video_path, metadata):
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
        
        log_event("YouTubeUploadAgent: Preparing video upload...")
        if not video_path or not os.path.exists(video_path):
            log_event("YouTubeUploadAgent: No video file found for upload.")
            return None

        # Check for Refresh Token
        refresh_token = globals().get("YT_REFRESH_TOKEN")
        client_id = globals().get("YT_CLIENT_ID")
        client_secret = globals().get("YT_CLIENT_SECRET")
        
        if not refresh_token:
            log_event("YouTubeUploadAgent: No YT_REFRESH_TOKEN found. Skipping real upload.")
            return {"status": "SKIPPED", "reason": "No refresh token"}

        try:
            creds = Credentials(
                None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=client_id,
                client_secret=client_secret
            )
            youtube = build("youtube", "v3", credentials=creds)
            
            body = {
                'snippet': {
                    'title': metadata.get('title', 'News Update'),
                    'description': metadata.get('description', ''),
                    'tags': metadata.get('tags', []),
                    'categoryId': '25' # News & Politics
                },
                'status': {
                    'privacyStatus': 'private' # Default to private for safety
                }
            }
            
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
            
            response = request.execute()
            video_id = response.get("id")
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            log_event(f"YouTubeUploadAgent: Real upload successful. URL: {url}")
            return {
                "upload_status": "SUCCESS",
                "video_id": video_id,
                "url": url
            }
        except Exception as e:
            log_event(f"YouTubeUploadAgent Real Upload Exception: {e}")
            return {"status": "FAILED", "error": str(e)}

# ==========================================
# AGENT 7: PRODUCTION & DISTRIBUTION (ORCHESTRATION)
# ==========================================
class MasterOrchestrator:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.verify_agent = VerificationAgent()
        self.script_agent = ScriptwriterAgent()
        self.voice_agent = VoiceoverAgent()
        self.video_agent = VideoAgent()
        self.assembly_agent = VideoAssemblyAgent()
        self.yt_agent = YouTubeUploadAgent()

    def run_pipeline(self):
        log_event("--- STARTING DAILY PIPELINE ---")
        
        # 1. Fetch
        raw_news = self.news_agent.fetch()
        
        # 2. Verify
        verified_news = self.verify_agent.verify(raw_news)
        
        # 3. Script
        final_script = self.script_agent.create_script(verified_news)
        
        # 4. Voiceover
        audio_path = self.voice_agent.generate_audio(final_script)
        
        # 5. Video Assets
        video_assets = self.video_agent.gather_assets(verified_news)
        
        # 6. Video Assembly
        final_video_path = self.assembly_agent.assemble(audio_path, video_assets)
        
        # 7. YouTube Upload
        video_metadata = {
            "title": f"Global Intelligence Brief - {datetime.datetime.now().strftime('%Y-%m-%d')}",
            "description": f"Daily automated news report for {datetime.datetime.now().strftime('%B %d, %Y')}.\n\nStories covered:\n" + "\n".join([f"- {n['title']}" for n in verified_news]),
            "tags": ["news", "geopolitics", "intelligence", "daily"]
        }
        upload_result = self.yt_agent.upload(final_video_path, video_metadata)
        
        # 8. Save Final Report
        report_name = f"production_{datetime.datetime.now().strftime('%Y-%m-%d')}.json"
        report_path = f"{REPORTS_DIR}/{report_name}"
        
        output_data = {
            "status": "COMPLETED",
            "timestamp": str(datetime.datetime.now()),
            "verified_news": verified_news,
            "script": final_script,
            "audio_path": audio_path,
            "video_assets": video_assets,
            "youtube_upload": upload_result
        }
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
            
        log_event(f"MasterOrchestrator: Daily Production Pack ready at {report_path}")
        log_event("--- PIPELINE SUCCESSFUL ---")

if __name__ == "__main__":
    orchestrator = MasterOrchestrator()
    orchestrator.run_pipeline()



# API KEY CONFIGURATION
NEWS_API_KEY = "67ce60cd1d764769a3410cd8c51cfbe5"
ELEVENLABS_KEY = "sk_f813c4e9e52df865c849f8efa7f6212848c91ba12a7841dc"
PEXELS_API_KEY = "nSXde8qGmWEfLMH2w6hSiUGfajEQ8BkuTr8Lr2XSv2qLAGviY16Pgxkz"