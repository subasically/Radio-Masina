import sys
sys.path.append('/root/AIRadioDJ/venv/lib/python3.12/site-packages')

import os
import pyshout
import time
from datetime import datetime
from announcement import generate_announcement_text, generate_tts, get_current_track  # Import your functions

# Connection details
ICECAST_URL = os.getenv("ICECAST_URL", "localhost")
ICECAST_PORT = os.getenv("ICECAST_PORT", 8000)
ICECAST_PASSWORD = os.getenv("ICECAST_PASSWORD", "hackme")
MOUNT_NAME = os.getenv("MOUNT_NAME", "/radio")

def is_dj_time():
    """Check if current time is within the 9am - 9pm range."""
    current_time = datetime.now().time()
    start_time = current_time.replace(hour=9, minute=0)
    end_time = current_time.replace(hour=21, minute=0)
    return start_time <= current_time <= end_time

def stream_audio(file_path):
    """Stream a file to Icecast."""
    client = pyshout.Shout()
    client.host = ICECAST_URL
    client.port = ICECAST_PORT
    client.user = "source"
    client.password = ICECAST_PASSWORD
    client.mount = MOUNT_NAME
    client.format = pyshout.FORMAT_MP3
    client.name = "RadioMašina AI DJ"

    # Open the audio file and stream it
    with open(file_path, 'rb') as audio:
        client.open()
        while chunk := audio.read(4096):
            client.send(chunk)
            client.sync()
        client.close()

def play_music_and_announcements():
    music_dir = "./music"  # Set your music directory
    music_files = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]
    
    # Loop through the music files
    for i in range(len(music_files)):
        current_music = os.path.join(music_dir, music_files[i])
        stream_audio(current_music)  # Stream current music

        # Get current and next track info
        now_playing, playing_next = get_current_track()
        if now_playing and playing_next:
            current_song_title = now_playing["song"]["title"]
            current_artist = now_playing["song"]["artist"]

            next_song_title = playing_next["song"]["title"]
            next_artist = playing_next["song"]["artist"]

            # Generate announcement text using OpenAI
            announcement_text = generate_announcement_text(
                current_song_title, current_artist, next_song_title, next_artist
            )
            if announcement_text:
                print(f"Generated announcement: {announcement_text}")
                voice = "nova"
                audio_data = generate_tts(announcement_text, voice)
                if audio_data:
                    audio_file_path = f"./announcement_{voice}.wav"
                    with open(audio_file_path, "wb") as f:
                        f.write(audio_data)
                    print(f"Announcement saved as: {audio_file_path}")

                    # Stream the announcement
                    stream_audio(audio_file_path)
                else:
                    print("Failed to generate audio data.")
            else:
                print("Failed to generate announcement text.")
        else:
            print("No current track information available.")

# Main loop
while True:
    if is_dj_time():
        play_music_and_announcements()
    else:
        print("Outside of DJ time, sleeping for an hour...")
        time.sleep(3600)  # Check again in an hour
