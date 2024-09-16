# 🎬 autocrop
Automagically crop a video clip within a video clip

![AutoCrop](https://github.com/paulpierre/autocrop/raw/main/autocrop.png)


## Overview
You know that feeling when you [spend 30 minutes looking for something](https://github.com/paulpierre/autocrop/blob/main/RESEARCH.MD) and realize "hm, no way no one has built it, if it's taking this long to find it.."
And then you just build it? Yep

## ⚡ Quickstart
Let's do some quick showing vs telling w/ an example:

❗ Note: This assumes you've ran through the setup below

Lets take a look at [this meme](https://www.instagram.com/reel/C_JHU6QNhm3/?hl=en) instagram reel from [@memes](https://www.instagram.com/memes/)

Here is the original video in the `./demo` directory:

<a href="https://imgur.com/L1gL7ue">
    <img src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_john_cena.png" alt="John Cena uncropped" style="width: 300px;">
</a>

We run `autocrop` with the following command:

```bash
python autocrop-cli.py --video_path ./demo/memes_ig_john_cena.mp4
```

And here is the output of `autocrop`:

<a href="https://imgur.com/OUsMztx">
    <img src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_john_cena_cropped.png" alt="John Cena cropped" style="width: 300px;">
</a>

This performs better on black backgrounds, you'll notice it defaulted to landscape vs square.

Let's try black background with this meme:

<a href="https://imgur.com/kD2jSOF">
    <img src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_southpark_poo.png" alt="Southpark uncropped" style="width: 300px;">
</a>

```bash
python autocrop-cli.py --video_path ./demo/memes_ig_southpark_poo.mp4
```
<a href="https://imgur.com/eHFcM1S">
    <img src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_southpark_poo_cropped.png" alt="Southpark Cropped" style="width: 300px;">
</a>

Nice 👌 much better.


## 🌟 Features

- Detects video content area automatically
- Crops to standard aspect ratios (9:16, 16:9, 1:1)
- Supports single video or batch processing
- Supports all black and white backgrounds
- Supports silencing original audio, adding audio from mp3
- Uses FFmpeg for high-quality video processing

## 🛠️ How It Works

1. **Frame Sampling**: Randomly selects frames from the video for analysis.
2. **Background Detection**: Identifies the background color of the video.
3. **Content Area Detection**: Locates the main content area within the video frames.
4. **Orientation Detection**: Determines if the content is portrait, landscape, or square.
5. **Aspect Ratio Adjustment**: Adjusts the crop area to match the closest standard aspect ratio.
6. **Video Cropping**: Uses FFmpeg to crop the video based on the detected area.

## 🏗️ Setup

```bash
git clone https://github.com/paulpierre/autocrop.git
cd autocrop
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 🚀 Usage

### CLI
```bash
# Process a single video
python autocrop-cli.py --video_path /path/to/video.mp4

# Process all MP4 files in a directory
python autocrop-cli.py --video_dir /path/to/video/directory

# Specify output path for single video processing
python autocrop-cli.py --video_path /path/to/video.mp4 --out /path/to/output.mp4

# Autocrop and add audio from mp3 on top of original audio
python autocrop.py --video_path /path/to/video.mp4 --out /path/to/output.mp4 --audio-track /path/to/audio.mp3 --audio-volume 0.4

# Silences original audio
python autocrop.py --video_path /path/to/video.mp4 --out /path/to/output.mp4 --silence-original-audio

# Silence original audio and replace with new audio
python autocrop.py --video_path /path/to/video.mp4 --out /path/to/output.mp4 --silence-original-audio --audio-track /path/to/audio.mp3 --audio-volume 0.4
```

### Python
```python
import autocrop

autocrop.process_video("/path/to/video.mp4", "/path/to/output.mp4")
```

## 🧩 Main Components

- `sample_frames()`: Extracts random frames from the video for analysis.
- `detect_background_color()`: Determines the background color of the video.
- `detect_video_area()`: Identifies the main content area within the video frames.
- `determine_orientation()`: Classifies the video orientation based on aspect ratio.
- `adjust_crop_to_ratio()`: Adjusts the crop area to match standard aspect ratios.
- `crop_video_with_ffmpeg()`: Uses FFmpeg to perform the actual video cropping.

## 🔧 Requirements
- MacOS / *nix
- Python 3.9+
- OpenCV
- NumPy
- FFmpeg (`brew install ffmpeg` on MacOS)

## 📝 Note

This script is designed to work best with videos that have a clear distinction between the main content and the background (i.e. Youtube Short or Instagram Reel) where there is branding and clutter surrounding the video. Results may vary for complex video scenes.

PR's welcome

## 🙌 Credits

Created by [@paulpierre](https://twitter.com/paulpierre) on X (Twitter)


## 📄 License

MIT License

Copyright (c) 2024 Paul Pierre

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
