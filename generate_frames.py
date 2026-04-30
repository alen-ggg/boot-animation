#!/usr/bin/env python3
"""
Generate custom Android boot animation frames with system failure and glitch effects.
Creates PNG frames for both animation sequences.
"""

import os
from PIL import Image, ImageDraw, ImageFilter
import random
import math

# Configuration
RESOLUTION = (1920, 1080)
FPS = 30
SYSTEM_FAILURE_DURATION = 2  # seconds
GLITCH_INSTALL_DURATION = 3  # seconds

SYSTEM_FAILURE_FRAMES = SYSTEM_FAILURE_DURATION * FPS  # 60 frames
GLITCH_INSTALL_FRAMES = GLITCH_INSTALL_DURATION * FPS  # 90 frames

def create_directories():
    """Create output directories for frame sequences."""
    os.makedirs("system_failure", exist_ok=True)
    os.makedirs("glitch_install", exist_ok=True)

def add_scan_lines(image, opacity=30):
    """Add horizontal scan line effect to image."""
    pixels = image.load()
    for y in range(0, RESOLUTION[1], 2):
        for x in range(RESOLUTION[0]):
            r, g, b, a = pixels[x, y]
            r = max(0, r - opacity)
            g = max(0, g - opacity)
            b = max(0, b - opacity)
            pixels[x, y] = (r, g, b, a)
    return image

def add_glitch_effect(image, intensity=0.1):
    """Add random pixel displacement glitch effect."""
    pixels = image.load()
    width, height = image.size
    
    for _ in range(int(width * height * intensity / 100)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        
        new_x = (x + offset_x) % width
        new_y = (y + offset_y) % height
        
        if 0 <= new_x < width and 0 <= new_y < height:
            pixels[x, y] = pixels[new_x, new_y]
    
    return image

def add_color_shift(image, channel_offset=20):
    """Add RGB channel separation for glitch effect."""
    r, g, b, a = image.split()
    
    # Shift channels slightly
    r = r.transform(r.size, Image.AFFINE, (1, 0, channel_offset, 0, 1, 0))
    b = b.transform(b.size, Image.AFFINE, (1, 0, -channel_offset, 0, 1, 0))
    
    return Image.merge("RGBA", (r, g, b, a))

def generate_system_failure_frame(frame_num):
    """Generate a system failure/error screen frame."""
    image = Image.new("RGBA", RESOLUTION, (0, 0, 0, 255))
    draw = ImageDraw.Draw(image)
    
    progress = frame_num / SYSTEM_FAILURE_FRAMES
    
    # Red error background
    red_intensity = int(100 + 155 * math.sin(progress * math.pi * 2))
    draw.rectangle([0, 0, RESOLUTION[0], RESOLUTION[1]], 
                   fill=(red_intensity, 0, 0, 255))
    
    # Add flickering effect
    if random.random() < 0.3:
        draw.rectangle([0, 0, RESOLUTION[0], RESOLUTION[1]], 
                       fill=(255, 50, 50, 200))
    
    # Error code text
    error_codes = [
        "SYSTEM_FAILURE",
        "KERNEL_PANIC",
        "FATAL_ERROR",
        "CRITICAL_STOP"
    ]
    error_text = random.choice(error_codes)
    draw.text((RESOLUTION[0]//2 - 200, RESOLUTION[1]//2 - 100), 
              error_text, fill=(255, 255, 255, 255))
    
    # Hex dump visualization
    for i in range(5):
        hex_line = "0x" + "".join(f"{random.randint(0, 255):02x}" for _ in range(16))
        draw.text((100, 300 + i * 80), hex_line, fill=(100, 255, 100, 200))
    
    # Add effects
    image = add_scan_lines(image, opacity=20)
    image = add_glitch_effect(image, intensity=5)
    
    # Random color shift
    if random.random() < 0.2:
        image = add_color_shift(image, channel_offset=10)
    
    return image

def generate_glitch_install_frame(frame_num):
    """Generate a glitchy app installation frame."""
    image = Image.new("RGBA", RESOLUTION, (20, 20, 30, 255))
    draw = ImageDraw.Draw(image)
    
    progress = frame_num / GLITCH_INSTALL_FRAMES
    
    # Background gradient
    for y in range(RESOLUTION[1]):
        color_val = int(20 + 50 * (y / RESOLUTION[1]))
        draw.line([(0, y), (RESOLUTION[0], y)], fill=(color_val, color_val, color_val + 20, 255))
    
    # App installation boxes with glitch
    app_names = ["System", "Gallery", "Camera", "Maps", "Gmail"]
    num_apps = min(len(app_names), int(1 + progress * len(app_names)))
    
    for i in range(num_apps):
        x = 200 + i * 300
        y = RESOLUTION[1] // 2 - 100
        
        # Glitch the box position
        if random.random() < 0.15:
            x += random.randint(-20, 20)
            y += random.randint(-20, 20)
        
        # App box
        draw.rectangle([x, y, x + 200, y + 200], 
                      outline=(100, 200, 255, 255), width=3)
        
        # Progress bar with glitch
        bar_width = 200 * progress
        if random.random() < 0.1:
            bar_width += random.randint(-30, 30)
        
        draw.rectangle([x + 10, y + 180, x + 10 + bar_width, y + 190],
                      fill=(100, 200, 255, 255))
        
        # App name with possible corruption
        app_text = app_names[i]
        if random.random() < 0.2:
            app_text = app_text[::-1]  # Reverse text glitch
        
        draw.text((x + 30, y + 100), app_text, fill=(200, 200, 200, 255))
    
    # Add effects
    image = add_scan_lines(image, opacity=15)
    image = add_glitch_effect(image, intensity=3)
    
    # Random chromatic aberration
    if random.random() < 0.15:
        image = add_color_shift(image, channel_offset=5)
    
    return image

def generate_all_frames():
    """Generate all animation frames."""
    print("Generating system_failure frames...")
    for i in range(SYSTEM_FAILURE_FRAMES):
        image = generate_system_failure_frame(i)
        image.save(f"system_failure/frame_{i:04d}.png")
        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{SYSTEM_FAILURE_FRAMES} frames generated")
    
    print("\nGenerating glitch_install frames...")
    for i in range(GLITCH_INSTALL_FRAMES):
        image = generate_glitch_install_frame(i)
        image.save(f"glitch_install/frame_{i:04d}.png")
        if (i + 1) % 15 == 0:
            print(f"  {i + 1}/{GLITCH_INSTALL_FRAMES} frames generated")
    
    print("\nFrame generation complete!")
    print(f"Total frames created: {SYSTEM_FAILURE_FRAMES + GLITCH_INSTALL_FRAMES}")

if __name__ == "__main__":
    create_directories()
    generate_all_frames()
    print("\nNext steps:")
    print("1. Review the generated frames in system_failure/ and glitch_install/")
    print("2. Run: zip -r bootanimation.zip desc.txt system_failure/ glitch_install/")
    print("3. Install on Android device (requires root)")
