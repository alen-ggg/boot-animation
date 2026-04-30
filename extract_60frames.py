#!/usr/bin/env python3
"""
Extract 60 frames from video and create bootanimation.zip for Samsung A04e
Specifications:
- 60 frames total
- 10 seconds duration (6 FPS)
- Resolution: 720x1600
- Video file: VID_20260430_082126_726.mp4

Requires: pip install opencv-python

Usage: python3 extract_60frames.py
"""

import cv2
import os
import shutil
import zipfile
from pathlib import Path

# Configuration
VIDEO_FILE = "VID_20260430_082126_726.mp4"
OUTPUT_DIR = "boot_animation_frames"
TOTAL_FRAMES_NEEDED = 60
TARGET_FPS = 6  # 60 frames / 10 seconds = 6 FPS
TARGET_WIDTH = 720
TARGET_HEIGHT = 1600

def extract_60_frames():
    """
    Extract exactly 60 frames from video, evenly distributed across the entire video.
    """
    # Clean up old frames
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    # Open video
    cap = cv2.VideoCapture(VIDEO_FILE)
    
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video file '{VIDEO_FILE}'")
        print("Make sure the video file exists in the current directory.")
        return False
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps
    
    print("="*60)
    print("Samsung A04e Boot Animation Extractor")
    print("="*60)
    print()
    print("📹 Video Information:")
    print(f"   File: {VIDEO_FILE}")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Total Frames: {total_frames}")
    print(f"   Duration: {duration:.2f} seconds")
    print()
    print("🎯 Boot Animation Settings:")
    print(f"   Target Frames: {TOTAL_FRAMES_NEEDED}")
    print(f"   Target FPS: {TARGET_FPS}")
    print(f"   Target Resolution: {TARGET_WIDTH}x{TARGET_HEIGHT}")
    print(f"   Boot Animation Duration: {TOTAL_FRAMES_NEEDED / TARGET_FPS} seconds")
    print()
    
    # Calculate frame indices to extract (evenly distributed)
    frame_indices = []
    for i in range(TOTAL_FRAMES_NEEDED):
        frame_idx = int((i / TOTAL_FRAMES_NEEDED) * total_frames)
        frame_indices.append(frame_idx)
    
    print(f"📊 Extracting {TOTAL_FRAMES_NEEDED} frames...")
    extracted_count = 0
    
    for i, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        
        if not ret:
            print(f"   ⚠️  Failed to extract frame {i}")
            continue
        
        # Resize to target resolution
        frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT), interpolation=cv2.INTER_LINEAR)
        
        # Save frame as PNG
        frame_name = f"frame_{i:04d}.png"
        frame_path = os.path.join(OUTPUT_DIR, frame_name)
        cv2.imwrite(frame_path, frame)
        extracted_count += 1
        
        # Progress indicator
        if (i + 1) % 10 == 0:
            print(f"   ✅ Extracted {i + 1}/{TOTAL_FRAMES_NEEDED} frames")
    
    cap.release()
    
    print()
    print(f"✅ Successfully extracted {extracted_count} frames!")
    return extracted_count

def create_desc_file():
    """
    Create desc.txt for Android boot animation.
    Format: width height fps
            p loop pause folder
    """
    desc_content = f"{TARGET_WIDTH} {TARGET_HEIGHT} {TARGET_FPS}\n"
    desc_content += f"p 0 0 {OUTPUT_DIR}\n"
    
    with open("desc.txt", "w") as f:
        f.write(desc_content)
    
    print()
    print("✅ Created desc.txt")
    print(f"   Resolution: {TARGET_WIDTH}x{TARGET_HEIGHT}")
    print(f"   FPS: {TARGET_FPS}")
    print(f"   Animation Duration: {TOTAL_FRAMES_NEEDED / TARGET_FPS} seconds")

def create_bootanimation_zip():
    """
    Create bootanimation.zip for Android installation.
    """
    print()
    print(f"📦 Creating bootanimation.zip...")
    
    with zipfile.ZipFile("bootanimation.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add desc.txt at root level
        zipf.write("desc.txt", "desc.txt")
        print(f"   ✅ Added desc.txt")
        
        # Add all frames in boot_animation_frames folder
        frame_files = sorted(Path(OUTPUT_DIR).glob("frame_*.png"))
        
        for i, frame_file in enumerate(frame_files):
            # Store in zip with folder structure
            arcname = f"{OUTPUT_DIR}/{frame_file.name}"
            zipf.write(frame_file, arcname)
            
            if (i + 1) % 10 == 0:
                print(f"   ✅ Added {i + 1}/{len(frame_files)} frames to ZIP")
    
    zip_size = os.path.getsize("bootanimation.zip") / (1024 * 1024)
    print(f"   ✅ Compressed {len(frame_files)} frames")
    print()
    print(f"✅ Created bootanimation.zip ({zip_size:.2f} MB)")

def print_installation_guide():
    """
    Print installation instructions.
    """
    print()
    print("="*60)
    print("✅ Boot Animation Ready!")
    print("="*60)
    print()
    print("📱 Installation Instructions (Samsung A04e):")
    print()
    print("Requirements:")
    print("  • Rooted Samsung A04e")
    print("  • USB Debugging enabled")
    print("  • ADB installed on your PC")
    print()
    print("Installation Steps:")
    print()
    print("1️⃣  Connect your phone via USB")
    print()
    print("2️⃣  Run these commands on your PC:")
    print()
    print("   adb push bootanimation.zip /system/media/bootanimation.zip")
    print("   adb shell chmod 644 /system/media/bootanimation.zip")
    print("   adb reboot")
    print()
    print("3️⃣  Your boot animation will play on next boot!")
    print()
    print("Alternative (without ADB):")
    print("  • Use Root Explorer app")
    print("  • Navigate to /system/media/")
    print("  • Copy bootanimation.zip there")
    print("  • Set permissions to 644")
    print("  • Reboot device")
    print()
    print("="*60)

if __name__ == "__main__":
    # Extract 60 frames
    frame_count = extract_60_frames()
    
    if frame_count == TOTAL_FRAMES_NEEDED:
        # Create descriptor
        create_desc_file()
        
        # Create ZIP
        create_bootanimation_zip()
        
        # Print guide
        print_installation_guide()
    else:
        print()
        print(f"❌ Failed: Expected {TOTAL_FRAMES_NEEDED} frames but got {frame_count}")
        print("Make sure the video file is valid.")
