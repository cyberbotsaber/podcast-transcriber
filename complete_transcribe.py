import re
import os
import sys
import yt_dlp
import whisper
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator


def extract_video_id(url):
    """Extract YouTube video ID from the given URL."""
    match = re.search(r"(?<=v=)[\w-]+", url)
    return match.group(0) if match else None


def check_transcript(video_url):
    """Fetch the transcript for the given YouTube video."""
    video_id = extract_video_id(video_url)
    if not video_id:
        print("Invalid YouTube URL!")
        sys.exit(1)

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        print("English transcript found.")
        return transcript_data

    except NoTranscriptFound:
        print("No English transcript available. Checking for auto-generated transcripts...")

        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['te'])
            print("Auto-generated Telugu transcript found. Translating to English...")
            return translate_transcript(transcript_data, target_lang='en')

        except NoTranscriptFound:
            print("No transcripts available. Downloading audio for Whisper transcription...")
            return None

        except TranscriptsDisabled:
            print("Transcripts are disabled for this video. Downloading audio for Whisper transcription...")
            return None

    except TranscriptsDisabled:
        print("Transcripts are disabled for this video. Downloading audio for Whisper transcription...")
        return None


def translate_transcript(transcript_data, target_lang='en'):
    """Translate the transcript text to the specified language."""
    translator = Translator()
    translated_transcript = []

    for entry in transcript_data:
        translated_text = translator.translate(entry['text'], dest=target_lang).text
        translated_transcript.append({'start': entry['start'], 'duration': entry['duration'], 'text': translated_text})

    print("Translation completed.")
    return translated_transcript


def download_audio(youtube_url, output_path="output.mp3"):
    """Download the audio from the given YouTube URL, ensuring no double extension issue."""
    base_filename = output_path.replace(".mp3", "")  # Remove any existing .mp3
    final_output = f"{base_filename}.mp3"  # Ensure correct format

    # Delete existing file if it exists
    if os.path.exists(final_output):
        os.remove(final_output)
        print(f"Deleted existing file: {final_output}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': base_filename,  # Let yt-dlp add the extension properly
        'ffmpeg_location': r'C:\ffmpeg\ffmpeg-master-latest-win64-gpl-shared\bin'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Check if yt-dlp appended an extra .mp3
    if os.path.exists(f"{base_filename}.mp3.mp3"):
        os.rename(f"{base_filename}.mp3.mp3", final_output)
    elif os.path.exists(f"{base_filename}.mp3"):
        os.rename(f"{base_filename}.mp3", final_output)

    print(f"Audio downloaded successfully as {final_output}")
    return final_output


def transcribe_audio(audio_path="output.mp3"):
    """Transcribe the downloaded audio using Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


def sanitize_filename(filename):
    """Remove invalid characters from a filename to make it safe for Windows."""
    invalid_chars = r'[<>:"/\\|?*]'  # Windows does not allow these characters in filenames
    sanitized = re.sub(invalid_chars, '', filename)  # Remove invalid characters
    return sanitized.strip()  # Trim extra spaces


def save_transcript(transcript_data, filename="transcript.txt"):
    """Save the transcript to a text file."""
    filename = sanitize_filename(filename)  # Ensure the filename is safe
    if not filename.endswith(".txt"):  # Ensure the correct extension
        filename += ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        for entry in transcript_data:
            if isinstance(entry, dict):  # If it's a YouTube transcript
                file.write(f"{entry['start']:.2f} - {entry['start'] + entry['duration']:.2f}: {entry['text']}\n")
            else:  # If it's a Whisper transcript (plain text)
                file.write(entry + "\n")

    print(f"Transcript saved to {filename}")


if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    transcript_data = check_transcript(video_url)

    if transcript_data is None:  # No transcript found, use Whisper
        audio_file = download_audio(video_url)
        transcript_data = transcribe_audio(audio_file)

    output_filename = input("Enter the name of the output file (e.g., transcript.txt): ")
    output_filename = sanitize_filename(output_filename)  # Fix invalid filename
    save_transcript(transcript_data, output_filename)

    print("Process completed successfully!")
