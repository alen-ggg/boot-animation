#!/usr/bin/env python3
"""
Generate preview videos from boot animation frame sequences.
Requires: pip install moviepy
"""

from moviepy.editor import ImageSequenceClip
import glob
import os

def create_preview(frame_dir, output_file, fps=30):
    """Create a video preview from PNG frame sequence."""
    # Get sorted list of frames
    frames = sorted(glob.glob(f"{frame_dir}/frame_*.png"))
    
    if not frames:
        print(f"No frames found in {frame_dir}")
        return
    
    print(f"Creating preview from {len(frames)} frames...")
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_file, verbose=False, logger=None)
    print(f"✅ Preview saved: {output_file}")

if __name__ == "__main__":
    # Install: pip install moviepy
    create_preview("system_failure", "system_failure_preview.mp4", fps=30)
    create_preview("glitch_install", "glitch_install_preview.mp4", fps=30)
