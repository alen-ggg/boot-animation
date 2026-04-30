# Android Boot Animation - System Failure & Glitch Theme

A custom Android boot animation featuring system failure screens and glitchy app installation effects.

## 🎬 Features

- **System Failure Animation** (2 seconds, 60 frames)
  - Red error screens
  - Flashing effects
  - Hex dump visualization
  - Scan line distortion
  - RGB channel separation glitches

- **Glitch Install Animation** (3 seconds, 90 frames)
  - Multiple app installation boxes
  - Glitchy progress bars
  - Corrupted text effects
  - Chromatic aberration
  - Random pixel displacement

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7+
- PIL/Pillow library
- FFmpeg (optional, for video previews)
- Rooted Android device (for installation)

### Generate Frames

```bash
# Install dependencies
pip install Pillow

# Generate all 150 animation frames
python3 generate_frames.py
```

This creates:
- `system_failure/` - 60 PNG frames
- `glitch_install/` - 90 PNG frames

### Create Boot Animation ZIP

```bash
# Package into bootanimation.zip
zip -r bootanimation.zip desc.txt system_failure/ glitch_install/
```

### Generate Video Preview (Optional)

```bash
# Install moviepy
pip install moviepy

# Generate MP4 preview videos
python3 generate_preview.py
```

Or use FFmpeg directly:

```bash
ffmpeg -framerate 30 -i system_failure/frame_%04d.png -c:v libx264 -pix_fmt yuv420p system_failure_preview.mp4
ffmpeg -framerate 30 -i glitch_install/frame_%04d.png -c:v libx264 -pix_fmt yuv420p glitch_install_preview.mp4
```

### Install on Android Device

**Using ADB (Android Debug Bridge):**

```bash
# Enable USB Debugging on your device first
# Then:
adb push bootanimation.zip /system/media/bootanimation.zip
adb shell chmod 644 /system/media/bootanimation.zip
adb reboot
```

**Using Recovery (if ADB doesn't work):**

1. Copy `bootanimation.zip` to your device's internal storage
2. Boot into Recovery mode
3. Use file manager to navigate to `/system/media/`
4. Replace existing `bootanimation.zip`
5. Reboot

**Using Root Explorer (if device is rooted):**

1. Open Root Explorer
2. Navigate to `/system/media/`
3. Copy `bootanimation.zip` there
4. Set permissions to `644`
5. Reboot

## 🎨 Customization

Edit `generate_frames.py` to customize:

- **Resolution**: Change `RESOLUTION = (1920, 1080)`
- **Frame Rate**: Change `FPS = 30`
- **Animation Duration**: Adjust `SYSTEM_FAILURE_DURATION` and `GLITCH_INSTALL_DURATION`
- **Colors**: Modify RGB values in frame generation functions
- **Effects Intensity**: Adjust `opacity`, `intensity`, `channel_offset` parameters
- **Text & Messages**: Edit `error_codes` and `app_names` lists

## 📁 File Structure

```
bootanimation.zip
├── desc.txt              # Animation descriptor
├── system_failure/       # System failure frames (60 PNGs)
└── glitch_install/       # Glitch install frames (90 PNGs)
```

### desc.txt Format

```
width height fps
p start_frame num_frames folder [repeat]
```

Example:
```
1920 1080 30
p 0 0 system_failure
p 0 0 glitch_install
```

- First line: Resolution (1920x1080) and frame rate (30 FPS)
- `p 0 0 system_failure` - Play system_failure frames once
- `p 0 0 glitch_install` - Play glitch_install frames once
- Use repeat count (e.g., `p 0 0 system_failure 2`) to loop

## 🐛 Troubleshooting

### Boot animation doesn't show

- Device is not rooted
- Wrong file permissions (should be 644)
- Wrong file location (must be `/system/media/bootanimation.zip`)
- Animation is too short (try adding repeat counts in desc.txt)

### Animation is slow or choppy

- Device has limited resources
- Reduce frame rate in desc.txt or re-generate with lower FPS
- Use simpler effects (reduce intensity values)

### Can't push file via ADB

- USB Debugging not enabled
- Device not connected properly
- Try: `adb devices` to verify connection
- Device needs to be rooted for `/system/media/` access

### Frame generation is slow

- Large resolution uses more CPU
- Reduce `RESOLUTION` for faster generation
- Disable expensive effects (glitch_effect, color_shift)

## 📝 Notes

- This requires a **rooted Android device**
- Backup original bootanimation.zip before replacing
- Animation will run every time device boots
- Some custom ROMs may not respect boot animations
- Total boot animation time: ~5 seconds (2s failure + 3s install)

## 📄 License

Free to use and modify for personal use.

## 🎬 Additional Resources

- [Android Boot Animation Documentation](https://source.android.com/docs/core/boot/boot-animation)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
