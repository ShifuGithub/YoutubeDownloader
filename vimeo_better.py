import subprocess
import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def ensure_directory_exists(folder):
    """Ensure the specified directory exists; create it if it doesn't."""
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_video_info(url):
    """Fetch video metadata using yt-dlp and return it as a dictionary."""
    try:
        command = ['yt-dlp', '--skip-download', '--print-json', url]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        video_info = json.loads(result.stdout)
        return video_info
    except subprocess.CalledProcessError as e:
        logging.error(f'Failed to get video info. Error: {e}')
        return None


def sanitize_filename(name):
    """Sanitize filename to avoid issues with filesystem."""
    return name.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"',
                                                                                                                   '-').replace(
        '<', '-').replace('>', '-').replace('|', '-')


def download_video(url, title, folder, quality='bestvideo[height<=?1080]'):
    """Download video and audio separately and return their filenames."""
    base_filename = sanitize_filename(title)
    video_filename = os.path.join(folder, f"{base_filename}_video.mp4")
    audio_filename = os.path.join(folder, f"{base_filename}_audio.m4a")

    try:
        video_command = ['yt-dlp', '-f', quality, '--merge-output-format', 'mp4', '--output', video_filename, url]
        audio_command = ['yt-dlp', '-f', 'bestaudio[ext=m4a]', '--output', audio_filename, url]

        logging.info(f"Downloading video: {title}")
        subprocess.run(video_command, check=True, text=True)
        logging.info(f"Downloading audio: {title}")
        subprocess.run(audio_command, check=True, text=True)

        return video_filename, audio_filename
    except subprocess.CalledProcessError as e:
        logging.error(f'Failed to download video or audio. Error: {e}')
        return None, None


def merge_video_audio(video_filename, audio_filename, title, folder):
    """Merge video and audio into a single file."""
    output_filename = os.path.join(folder, sanitize_filename(title) + ".mp4")
    try:
        if video_filename and audio_filename:
            ffmpeg_command = ['ffmpeg', '-i', video_filename, '-i', audio_filename, '-c:v', 'copy', '-c:a', 'aac',
                              '-strict', 'experimental', output_filename]
            subprocess.run(ffmpeg_command, check=True, text=True)
            logging.info(f"Merged video and audio into: {output_filename}")
            return output_filename
        else:
            logging.error("Missing video or audio filename.")
            return None
    except subprocess.CalledProcessError as e:
        logging.error(f'Failed to merge video and audio. Error: {e}')
        return None


def cleanup_files(*files):
    """Delete temporary files."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            logging.info(f"Deleted temporary file: {file}")


def download_and_process_video(url):
    """Main function to handle the download and processing of a video."""
    output_folder = 'downloaded_videos'
    ensure_directory_exists(output_folder)
    video_info = get_video_info(url)
    if video_info:
        title = video_info.get('title', 'Untitled Video')
        video_filename, audio_filename = download_video(url, title, output_folder)
        if video_filename and audio_filename:
            output_filename = merge_video_audio(video_filename, audio_filename, title, output_folder)
            if output_filename:
                logging.info(f"Process completed successfully: {output_filename}")
                cleanup_files(video_filename, audio_filename)  # Delete temporary files
            else:
                logging.error("Failed to merge video and audio.")
        else:
            logging.error("Download failed.")
    else:
        logging.error("Could not fetch video info.")


# Example usage
video_url = 'https://player.vimeo.com/video/898890451' # next 898883421 test
download_and_process_video(video_url)
