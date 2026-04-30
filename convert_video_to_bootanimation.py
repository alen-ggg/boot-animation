#!/usr/bin/env python3
"""
Extract frames from video and convert to Android boot animation.
Requires: pip install opencv-python
"""

import cv2
import os
import shutil
from pathlib import Path

# Video configuration
VIDEO_FILE = "VID_20260430_082126_726.mp4"
OUTPUT_DIR = "boot_animation_frames"
VIDEO_FPS = 60
VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1600

# Samsung A04e boot animation specs
BOOT_ANIMATION_WIDTH = 720
BOOT_ANIMATION_HEIGHT = 1600
BOOT_ANIMATION_FPS = 30  # Optimize for device

def extract_frames_from_video():
    """
    Extract frames from video file.
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
    
    print(f"Video Info:")
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  Total Frames: {total_frames}")
    print(f"  Duration: {total_frames / fps:.2f} seconds")
    print()
    
    # Extract frames
    print(f"Extracting frames to {OUTPUT_DIR}/...")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Resize to boot animation resolution if needed
        if (width, height) != (BOOT_ANIMATION_WIDTH, BOOT_ANIMATION_HEIGHT):
            frame = cv2.resize(frame, (BOOT_ANIMATION_WIDTH, BOOT_ANIMATION_HEIGHT), interpolation=cv2.INTER_LINEAR)
        
        # Save frame as PNG
        frame_name = f"frame_{frame_count:04d}.png"
        frame_path = os.path.join(OUTPUT_DIR, frame_name)
        cv2.imwrite(frame_path, frame)
        
        frame_count += 1
        
        # Progress indicator
        if (frame_count) % 30 == 0:
            print(f"  Extracted {frame_count}/{total_frames} frames")
    
    cap.release()
    
    print(f"✅ Extracted {frame_count} frames successfully!")
    return frame_count

def create_desc_file(frame_count):
    """
    Create desc.txt for Android boot animation.
    Format: width height fps
            p loop pause folder
    """
    desc_content = f"{BOOT_ANIMATION_WIDTH} {BOOT_ANIMATION_HEIGHT} {BOOT_ANIMATION_FPS}\n"
    desc_content += f"p 0 0 {OUTPUT_DIR}\n"
    
    with open("desc.txt", "w") as f:
        f.write(desc_content)
    
    print(f"\n✅ Created desc.txt")
    print(f"   Resolution: {BOOT_ANIMATION_WIDTH}x{BOOT_ANIMATION_HEIGHT}")
    print(f"   FPS: {BOOT_ANIMATION_FPS}")
    print(f"   Frames: {frame_count}")
    print(f"   Duration: {frame_count / BOOT_ANIMATION_FPS:.2f} seconds")

def create_bootanimation_zip():
    """
    Create bootanimation.zip for Android.
    """
    import zipfile
    
    print(f"\nCreating bootanimation.zip...")
    
    with zipfile.ZipFile("bootanimation.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add desc.txt
        zipf.write("desc.txt")
        
        # Add all frames
        frame_files = sorted(Path(OUTPUT_DIR).glob("frame_*.png"))
        for i, frame_file in enumerate(frame_files):
            zipf.write(frame_file, frame_file.name)
            if (i + 1) % 30 == 0:
                print(f"  Compressed {i + 1}/{len(frame_files)} frames")
    
    print(f"✅ Created bootanimation.zip")

if __name__ == "__main__":
    print("="*60)
    print("Android Boot Animation Video Converter")
    print(f"Target: Samsung A04e (720x1600)")
    print("="*60)
    print()
    
    # Extract frames
    frame_count = extract_frames_from_video()
    
    if frame_count:
        # Create descriptor
        create_desc_file(frame_count)
        
        # Create ZIP
        create_bootanimation_zip()
        
        print()
        print("="*60)
        print("✅ Boot Animation Ready!")
        print("="*60)
        print()
        print("📱 Installation Instructions (Requires Root):")
        print()
        print("1. Enable USB Debugging on your Samsung A04e")
        print("2. Connect device via USB")
        print("3. Run these commands:")
        print()
        print("   adb push bootanimation.zip /system/media/bootanimation.zip")
        print("   adb shell chmod 644 /system/media/bootanimation.zip")
        print("   adb reboot")
        print()
        print("Or use Root Explorer to manually copy to /system/media/")
        print()
    else:
        print("❌ Failed to extract frames from video.")
        print(f"Make sure '{VIDEO_FILE}' exists and is a valid video file.")
