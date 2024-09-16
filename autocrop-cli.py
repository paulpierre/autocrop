import autocrop
import argparse
import os
import glob
import logging

# Configure logging for verbose output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    print(autocrop.BANNER)

    parser = argparse.ArgumentParser(description='Autocrop video to standard aspect ratio')
    parser.add_argument('--video_path', help='Path to input video')
    parser.add_argument('--video_dir', help='Directory containing MP4 files to process')
    parser.add_argument('--out', dest='output_path', help='Path to output video (only used with --video_path)')
    parser.add_argument('--audio-track', help='Path to audio track to add to the video')
    parser.add_argument('--audio-volume', type=float, default=0.1, help='Volume level for added audio track (default: 0.1)')
    parser.add_argument('--silence-audio', action='store_true', help='Remove original audio from the output video')

    args = parser.parse_args()

    if args.video_path and args.video_dir:
        parser.error("Please specify either --video_path or --video_dir, not both.")
    elif args.video_path:
        # Process single video
        output_path = args.output_path or os.path.splitext(args.video_path)[0] + "_cropped.mp4"
        autocrop.process_video(args.video_path, output_path, args.audio_track, args.audio_volume, args.silence_audio)
    elif args.video_dir:
        # Process all .mp4 files in the specified directory
        mp4_files = glob.glob(os.path.join(args.video_dir, '*.mp4'))
        if not mp4_files:
            logging.error(f"No .mp4 files found in the directory: {args.video_dir}")
        else:
            for video_path in mp4_files:
                output_path = os.path.splitext(video_path)[0] + "_cropped.mp4"
                autocrop.process_video(video_path, output_path, args.audio_track, args.audio_volume, args.silence_audio)
    else:
        parser.error("Please specify either --video_path or --video_dir.")