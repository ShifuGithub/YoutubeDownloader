import subprocess
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Single Vimeo video URL for testing
video_url = 'https://player.vimeo.com/video/897001352'
video_title = 'LeanAgencyModel'
video_id = video_url.split('/')[-1]

def download_and_convert_video(video_url, video_id):
    logging.info(f'Starting download for {video_url}')

    # Define filenames for video and audio based on video ID
    video_filename = f"{video_id}_video.mp4"
    audio_filename = f"{video_id}_audio.m4a"
    output_filename = f"video_title.mp4"

    try:
        # Download the best video and audio separately
        video_command = ['yt-dlp', '-f', 'bestvideo[ext=mp4]', '--output', video_filename, video_url]
        audio_command = ['yt-dlp', '-f', 'bestaudio[ext=m4a]', '--output', audio_filename, video_url]

        subprocess.run(video_command, check=True, text=True)
        subprocess.run(audio_command, check=True, text=True)

        # Check if both files exist before attempting to merge
        if os.path.exists(video_filename) and os.path.exists(audio_filename):
            # Use ffmpeg to merge video and audio
            ffmpeg_command = ['ffmpeg', '-i', video_filename, '-i', audio_filename, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_filename]
            subprocess.run(ffmpeg_command, check=True, text=True)
            logging.info(f'Successfully downloaded and converted {video_url}')
        else:
            logging.error(f'Error: Missing video or audio file for {video_url}.')

    except subprocess.CalledProcessError as e:
        logging.error(f'Failed to process video {video_url}. Error: {e}')
    except Exception as e:
        logging.error(f'An unexpected error occurred with {video_url}. Error: {e}')

# Start the download and conversion process for the provided video
download_and_convert_video(video_url, video_id)
