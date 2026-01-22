"""
Demo News Broadcast with AI Presenter
Creates a demo showing the presenter concept
"""

import json
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np

try:
    from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
except ImportError:
    from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip

print("🎬 Creating DEMO News Broadcast...\n")

# Load production report
with open("d:/interest/automated_production/reports/production_2026-01-22.json", "r") as f:
    report = json.load(f)

# Create a demo presenter image (news studio style)
def create_demo_presenter_image():
    """Create a demo presenter placeholder image"""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=(20, 40, 80))
    draw = ImageDraw.Draw(img)
    
    # Create news desk background
    # Top third - news graphics background
    for y in range(0, 240):
        color = (25 + y//3, 45 + y//3, 90 + y//2)
        draw.rectangle([0, y, width, y+1], fill=color)
    
    # Middle - presenter area (darker)
    draw.rectangle([0, 240, width, 480], fill=(30, 50, 90))
    
    # Bottom - news desk
    for y in range(480, 720):
        shade = 480 - (y - 480)//4
        color = (shade//8, shade//6, shade//4)
        draw.rectangle([0, y, width, y+1], fill=color)
    
    # Add graphics elements
    # Global Brief logo area
    draw.rectangle([50, 50, 400, 190], fill=(200, 50, 50), outline=(255, 255, 255), width=3)
    draw.rectangle([880, 50, 1230, 190], fill=(0, 100, 200), outline=(255, 255, 255), width=3)
    
    # Presenter silhouette placeholder
    center_x, center_y = 640, 340
    draw.ellipse([center_x-120, center_y-150, center_x+120, center_y-30], fill=(60, 80, 120))
    draw.ellipse([center_x-100, center_y-180, center_x+100, center_y-140], fill=(80, 100, 140))
    
    # Add text overlays
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_medium = ImageFont.truetype("arial.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Main title
    draw.text((100, 90), "GLOBAL", fill=(255, 255, 255), font=font_large)
    draw.text((100, 140), "INTELLIGENCE", fill=(255, 200, 200), font=font_medium)
    
    # Right side graphics
    draw.text((920, 90), "LIVE", fill=(255, 50, 50), font=font_large)
    draw.text((920, 140), "24 NEWS", fill=(255, 255, 255), font=font_medium)
    
    # Bottom ticker bar
    draw.rectangle([0, 660, width, 720], fill=(200, 0, 0))
    draw.text((20, 675), "● BREAKING NEWS ● GEOPOLITICAL UPDATES ● GLOBAL INTELLIGENCE BRIEF", 
              fill=(255, 255, 255), font=font_medium)
    
    # Save
    img_path = "d:/interest/automated_production/videos/demo_presenter_frame.png"
    img.save(img_path)
    return img_path

print("📸 Creating demo presenter frame...")
presenter_img_path = create_demo_presenter_image()
print(f"   ✅ Created: {presenter_img_path}")

# Load the audio
audio_path = "d:/interest/automated_production/audio/demo_voiceover.mp3"
audio = AudioFileClip(audio_path)
duration = audio.duration

print(f"\n🎵 Audio duration: {duration:.1f} seconds")

# Create video from presenter image
print("\n🎬 Assembling demo broadcast...")
presenter_clip = ImageClip(presenter_img_path, duration=duration)

# Add audio
if hasattr(presenter_clip, 'with_audio'):
    final_clip = presenter_clip.with_audio(audio)
else:
    final_clip = presenter_clip.set_audio(audio)

# Export
output_path = "d:/interest/automated_production/videos/DEMO_news_broadcast.mp4"
print(f"\n📺 Exporting to: {output_path}")

final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

print("\n" + "="*70)
print("✅ DEMO NEWS BROADCAST CREATED!")
print("="*70)
print(f"\n📁 Demo Video: {output_path}")
print("\n📋 This demo shows:")
print("   ✓ Professional news studio layout")
print("   ✓ AI female narrator voice")
print("   ✓ News graphics and branding")
print("   ✓ Breaking news ticker")
print("\n💡 With D-ID API, the presenter will be:")
print("   → A realistic female news anchor")
print("   → Lip-synced perfectly to the audio")
print("   → Natural facial expressions and movements")
print("\n🚀 Set up D-ID to get the full realistic presenter!")
print("   See: D-ID_SETUP_GUIDE.md")
