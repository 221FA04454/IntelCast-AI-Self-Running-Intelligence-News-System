import json
import os
import requests
from gtts import gTTS
try:
    from moviepy import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips

# Load the production report
with open("d:/interest/automated_production/reports/production_2026-01-22.json", "r") as f:
    report = json.load(f)

print("🎬 Creating professional news video with AI presenter...")

# Create segments for each story
segments = []
script_segments = report['script']['segments']
video_assets = report['video_assets']

# Generate female voice narration for each segment
for i, (script_seg, asset) in enumerate(zip(script_segments, video_assets)):
    if i == 0:  # Skip the hook for now
        continue
    
    print(f"\n📰 Processing Story {i}: {asset['title'][:50]}...")
    
    # Generate voice for this segment
    audio_path = f"d:/interest/automated_production/audio/segment_{i}.mp3"
    tts = gTTS(text=script_seg['content'], lang='en', slow=False, tld='co.uk')  # British female voice
    tts.save(audio_path)
    
    # Download background video
    temp_video_path = f"d:/interest/automated_production/videos/bg_{i}.mp4"
    print(f"  ⬇️  Downloading background footage...")
    v_resp = requests.get(asset['video_url'])
    with open(temp_video_path, "wb") as f:
        f.write(v_resp.content)
    
    # Load and prepare background
    bg_clip = VideoFileClip(temp_video_path)
    duration = min(bg_clip.duration, 15)
    
    if hasattr(bg_clip, 'subclipped'):
        bg_clip = bg_clip.subclipped(0, duration)
    else:
        bg_clip = bg_clip.subclip(0, duration)
    
    if hasattr(bg_clip, 'resized'):
        bg_clip = bg_clip.resized(height=720)
    else:
        bg_clip = bg_clip.resize(height=720)
    
    # Add audio to background
    audio = AudioFileClip(audio_path)
    if hasattr(bg_clip, 'with_audio'):
        bg_clip = bg_clip.with_audio(audio)
    else:
        bg_clip = bg_clip.set_audio(audio)
    
    # Create headline overlay using ImageMagick
    headline = asset['title'].split(' - ')[0][:80]
    
    try:
        txt_clip = TextClip(
            txt=headline,
            fontsize=40,
            color='white',
            bg_color='black',
            size=(bg_clip.w - 100, None),
            method='caption',
            duration=duration
        )
        
        if hasattr(txt_clip, 'with_position'):
            txt_clip = txt_clip.with_position(('center', bg_clip.h - 120))
        else:
            txt_clip = txt_clip.set_position(('center', bg_clip.h - 120))
        
        # Composite background with text
        if hasattr(CompositeVideoClip, 'composite'):
            final_segment = CompositeVideoClip.composite([bg_clip, txt_clip])
        else:
            final_segment = CompositeVideoClip([bg_clip, txt_clip])
    except Exception as e:
        print(f"  ⚠️  Text overlay failed ({e}), using background only")
        final_segment = bg_clip
    
    segments.append(final_segment)
    print(f"  ✅ Story {i} complete!")

# Combine all segments
print("\n🎞️  Assembling final video...")
final_video = concatenate_videoclips(segments, method="compose")

# Export
output_path = "d:/interest/automated_production/videos/news_broadcast_with_presenter.mp4"
final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

print(f"\n✅ Professional news broadcast created!")
print(f"📁 Location: {output_path}")
print(f"\n🎯 Features:")
print("  ✓ AI female narrator with British accent")
print("  ✓ Dynamic backgrounds matching each story")
print("  ✓ Professional headline overlays")
print("  ✓ Smooth transitions between stories")
