import cv2
import numpy as np
import os
import subprocess
import logging
import argparse
import random
import glob

BANNER ="""
                     ██
                     ██
 ▄█▀██▄ ▀███  ▀███ ██████  ▄██▀██▄ ▄██▀██▀███▄███  ▄██▀██▄▀████████▄
██   ██   ██    ██   ██   ██▀   ▀███▀  ██  ██▀ ▀▀ ██▀   ▀██ ██   ▀██
 ▄█████   ██    ██   ██   ██     ███       ██     ██     ██ ██    ██
██   ██   ██    ██   ██   ██▄   ▄███▄    ▄ ██     ██▄   ▄██ ██   ▄██
▀████▀██▄ ▀████▀███▄ ▀████ ▀█████▀ █████▀▄████▄    ▀█████▀  ██████▀
Automatically detect crop area of any video // by @paulpierre on X
                                                           ▄████▄

"""


# Configure logging for verbose output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define standard aspect ratios
ASPECT_RATIOS = {
    'portrait': 9/16,  # 9:16
    'landscape': 16/9,  # 16:9
    'square': 1/1,     # 1:1
}

# Define margin to increase crop area
MARGIN = 0  # pixels

def sample_frames(video_path, num_samples=10):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []

    for _ in range(num_samples):
        frame_idx = random.randint(0, frame_count - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    cap.release()
    return frames

def detect_background_color(frames):
    borders = []
    for frame in frames:
        if len(frame.shape) == 3:  # Color image
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        borders.extend(frame[0, :])  # Top border
        borders.extend(frame[-1, :])  # Bottom border
        borders.extend(frame[:, 0])  # Left border
        borders.extend(frame[:, -1])  # Right border

    background_color = np.median(borders)
    is_white_background = background_color > 240  # Threshold for considering background as white

    return background_color, is_white_background

def detect_video_area(frames, background_color, is_white_background):
    masks = []
    for frame in frames:
        if len(frame.shape) == 3:  # Color image
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if is_white_background:
            mask = frame < (background_color - 10)  # Invert the condition for white background
        else:
            mask = frame > (background_color + 10)

        masks.append(mask)

    combined_mask = np.logical_or.reduce(masks)
    contours, _ = cv2.findContours(combined_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    return x, y, w, h

def determine_orientation(w, h):
    aspect_ratio = w / h
    if 0.95 <= aspect_ratio <= 1.05:
        return 'square'
    elif aspect_ratio > 1:
        return 'landscape'
    else:
        return 'portrait'

def adjust_crop_to_ratio(crop, target_ratio, frame_width, frame_height):
    x, y, w, h = crop

    # Add margin
    margin = min(MARGIN, min(w, h) // 10)  # Use smaller margin for small crops
    x = max(0, x - margin)
    y = max(0, y - margin)
    w = min(frame_width - x, w + 2 * margin)
    h = min(frame_height - y, h + 2 * margin)

    current_ratio = w / h

    if abs(current_ratio - target_ratio) < 0.1:  # If close to target ratio, keep as is
        return x, y, w, h

    if current_ratio > target_ratio:
        # Too wide, adjust width
        new_w = int(h * target_ratio)
        x += (w - new_w) // 2
        w = new_w
    else:
        # Too tall, adjust height
        new_h = int(w / target_ratio)
        y += (h - new_h) // 2
        h = new_h

    return x, y, w, h

def crop_video_with_ffmpeg(video_path, output_path, x, y, w, h):
    logging.info(f"Cropping video: x={x}, y={y}, w={w}, h={h}")
    ffmpeg_command = [
        'ffmpeg', '-i', video_path, '-filter:v', f'crop={w}:{h}:{x}:{y}',
        '-c:a', 'copy', output_path
    ]
    subprocess.run(ffmpeg_command, check=True)

def process_video(video_path, output_path):
    logging.info(f"Processing video: {video_path}")

    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    frames = sample_frames(video_path, num_samples=20)
    background_color, is_white_background = detect_background_color(frames)
    logging.info(f"Detected background color: {background_color}, Is white background: {is_white_background}")

    video_area = detect_video_area(frames, background_color, is_white_background)

    if not video_area:
        logging.error("No suitable video area found")
        return

    x, y, w, h = video_area
    orientation = determine_orientation(w, h)
    target_ratio = ASPECT_RATIOS[orientation]
    logging.info(f"Detected video area orientation: {orientation}, aspect ratio: {w/h:.2f}")

    final_crop = adjust_crop_to_ratio(video_area, target_ratio, frame_width, frame_height)
    crop_video_with_ffmpeg(video_path, output_path, *final_crop)
    logging.info(f"Video cropped and saved to {output_path}")