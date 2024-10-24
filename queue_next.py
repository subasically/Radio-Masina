import random
import time
import sys
from music_manager import index_music_directory, get_song_metadata
from announcement_generator import generate_announcement_text
from tts_generator import generate_tts_audio
from logger import log
from liquidsoap_client import LiquidsoapClient
from pathlib import Path
# from normalize_audio import normalize_audio

def queue_next(current_title, current_artist):
    """Queue the next announcement and song."""
    # log("Queuing the next announcement and song...", "queue_next")
    log("Current song: {} - {}".format(current_title, current_artist), "queue_next")

    # Connect to Liquidsoap server
    client = LiquidsoapClient(queue="play")

    # Create the playlist
    songs = index_music_directory()
    random.shuffle(songs)

    # Get the next song
    next_song = songs[0]
    next_song_metadata = get_song_metadata(next_song)
    
    log(f"Next song: {next_song_metadata['title']} - {next_song_metadata['artist']}", "queue_next")

    # Generate the announcement
    if current_artist and current_title:    
        announcement_text = generate_announcement_text(
            current_title,
            current_artist,
            next_song_metadata["title"],
            next_song_metadata["artist"],
        )
    else:
        announcement_text = generate_announcement_text(
            None,
            None,
            next_song_metadata["title"],
            next_song_metadata["artist"],
        )
    log(f"Announcement: {announcement_text}", "queue_next")
    tts_path = generate_tts_audio(announcement_text, filename="announcement.mp3")
    
    # normalize_audio(tts_path)

    # Queue the announcement and the next song
    if tts_path:
        # log(f"Queueing announcement", "queue_next")
        client.queue_song(tts_path, f"DJ Mašina - Announcement - {tts_path}", queue="play")
    
    wait_time = 5  # Time in seconds to wait before playing the next song
    log(f"Waiting for {wait_time} seconds...", "queue_next")
    time.sleep(wait_time)
    
    log(f"Queueing next song: {next_song_metadata['title']} - {next_song_metadata['artist']}", "queue_next")
    client.queue_song(next_song, f"{next_song_metadata['title']} - {next_song_metadata['artist']}", queue="play")

if __name__ == "__main__":
    log("Starting queue_next.py script...", "queue_next")
    current_title = sys.argv[1] if len(sys.argv) > 1 else ""
    current_artist = sys.argv[2] if len(sys.argv) > 2 else ""
    queue_next(current_title, current_artist)
    log("Finished queue_next.py script.", "queue_next")