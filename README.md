# 🎬 autocrop
Automagically crop a video clip within a video clip

![AutoCrop](https://github.com/paulpierre/autocrop/raw/main/autocrop.png)


# 🎬 AutoCrop Video


## Overview
You know that feeling when you [spend 30 minutes looking for something](https://github.com/paulpierre/autocrop/blob/main/RESEARCH.MD) and realize "hm, no way no one has built it, if it's taking this long to find it.."
And then you just build it? Yep

## ⚡ Quickstart
Let's do some quick showing vs telling w/ an example:

❗ Note: This assumes you've ran through the setup below

Lets take a look at [this meme](https://www.instagram.com/reel/C_JHU6QNhm3/?hl=en) instagram reel from [@memes](https://www.instagram.com/memes/)

Here is the original video in the `./demo` directory:

<video src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_john_cena.mp4" />

We run `autocrop` with the following command:

```bash
python autocrop-cli.py --video_path ./demo/memes_ig_john_cena.mp4
```

And here is the output of `autocrop`:

<video src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_john_cena_cropped.mp4" />

This performs better on black backgrounds, you'll notice it defaulted to landscape vs square.

Let's try black background with this meme:

<video src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_southpark_poo.mp4" />
```bash
python autocrop-cli.py --video_path ./demo/memes_ig_southpark_poo.mp4
```

<video src="https://github.com/paulpierre/autocrop/blob/main/demo/memes_ig_southpark_poo_cropped.mp4" />

Nice 👌 much better.



## 🌟 Features

- Detects video content area automatically
- Crops to standard aspect ratios (9:16, 16:9, 1:1)
- Supports single video or batch processing
- Supports all black and white backgrounds
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
bash
# Process a single video
python autocrop-cli.py --video_path /path/to/video.mp4

# Process all MP4 files in a directory
python autocrop-cli.py --video_dir /path/to/video/directory

# Specify output path for single video processing
python autocrop-cli.py --video_path /path/to/video.mp4 --out /path/to/output.mp4
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
- FFmpeg

## 📝 Note

This script is designed to work best with videos that have a clear distinction between the main content and the background (i.e. Youtube Short or Instagram Reel) where there is branding and clutter surrounding the video. Results may vary for complex video scenes.

PR's welcome

## 🙌 Credits

Created by [@paulpierre](https://twitter.com/paulpierre) on X (Twitter)
