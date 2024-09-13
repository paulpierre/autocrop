# Cropdetect

Prior to rolling up my own solution, I looked into existing ones.

Here are two interesting leads:
[Auto crop](https://superuser.com/questions/810471/remove-mp4-video-top-and-bottom-black-bars-using-ffmpeg)
[Yolov8 approach](https://medium.com/@maciek99/unlocking-the-power-of-yolov8-in-python-auto-reframe-aka-smart-video-crop-c30644c34481)

Here is a bash script I found that uses ffmpeg to detect the crop values and then uses ffplay to display the video with the new crop values. It's not perfect but it's a good starting point.

```bash
#!/bin/bash

# Check if a video file argument is passed
if [ -z "$1" ]; then
    echo "Usage: $0 <video file>"
    exit 1
fi

# Assign the first argument as the video file
video_file="$1"

# Run ffmpeg to detect crop values
output=$(ffmpeg -ss 5 -i "$video_file" -vframes 6 -vf cropdetect -f null - 2>&1)

# Extract the crop value from the output using grep and awk
crop=$(echo "$output" | grep 'crop=' | awk -F'crop=' '{print $2}' | head -n 1)

# Check if crop value was found
if [ -z "$crop" ]; then
    echo "Failed to detect crop values"
    exit 1
fi

# Split the crop value into width, height, x, and y
IFS=':' read -r width height x y <<< "$crop"

# Add 100 to the Y value
new_y=$((y + 100))

# Construct the new crop value
new_crop="${width}:${height}:${x}:${new_y}"

# Run ffplay with the new crop value
ffplay -vf crop=$new_crop "$video_file"
```