import random
import time
import threading
import queue
from music_manager import index_music_directory, get_song_metadata
from announcement_generator import (
    generate_start_introduction,
    generate_announcement_text,
)
from audio_streamer import play_song
from tts_generator import generate_tts_audio
from pydub import AudioSegment
from config import INTRO_SONG_PATH
from logger import log
from liquidsoap_client import LiquidsoapClient


def play_intro_with_fade(intro_text, intro_song_path):
    """Play the introduction with a fade-in effect over the intro song."""
    intro_filename = "introduction.mp3"

    if intro_song_path is None or intro_song_path == "":
        if generate_tts_audio(intro_text, intro_filename):
            log("No intro song path provided. Playing the introduction alone.")
            intro_audio = AudioSegment.from_file(intro_filename)
            return intro_audio
    else:
        intro_audio = AudioSegment.from_file(intro_song_path)
        if generate_tts_audio(intro_text, intro_filename):
            intro_tts_audio = AudioSegment.from_file(intro_filename)
            combined_audio = intro_tts_audio.overlay(intro_audio, position=0)
            return combined_audio


def create_playlist():
    """Create a playlist from the indexed songs in the music directory."""
    log("Creating a new playlist.")
    songs = index_music_directory()
    random.shuffle(songs)
    return songs


def stream_from_queue(client, q):
    """Stream items from the queue to the Liquidsoap server."""
    while True:
        item = q.get()
        if item is None:
            break
        song, title, artist = item
        play_song(client, song, title, artist)
        q.task_done()


def queue_songs_and_intros(q, songs, start_index=0, batch_size=1):
    """Queue a batch of songs and their intros."""
    previous_song_metadata = None
    for i in range(start_index, min(start_index + batch_size, len(songs))):
        song = songs[i]
        metadata = get_song_metadata(song)
        if metadata:
            if previous_song_metadata:
                announcement_text = generate_announcement_text(
                    previous_song_metadata["title"],
                    previous_song_metadata["artist"],
                    metadata["title"],
                    metadata["artist"],
                )
                tts_filename = f"next_song_intro_{i}.mp3"
                if generate_tts_audio(announcement_text, tts_filename):
                    q.put((tts_filename, "Announcement", "DJ Mašina"))
            q.put((song, metadata["title"], metadata["artist"]))
            previous_song_metadata = metadata
        else:
            log(f"Skipping song due to missing metadata: {song}")


def main():
    """Main function to run the AI DJ streaming service."""
    log("Creating a new playlist.")
    songs = create_playlist()

    # Generate and play the introduction
    intro_text = generate_start_introduction()
    intro_audio = play_intro_with_fade(intro_text, INTRO_SONG_PATH)

    # Connect to Liquidsoap server
    client = LiquidsoapClient()
    client.connect()

    # Create a queue for songs and intros
    q = queue.Queue()

    # Add the introduction to the queue
    if intro_audio:
        intro_filename = "combined_intro.mp3"
        intro_audio.export(intro_filename, format="mp3")
        q.put((intro_filename, "Introduction", "DJ Mašina"))

    # Queue initial batch of songs and intros
    queue_songs_and_intros(q, songs, start_index=0, batch_size=1)

    # Start streaming from the queue
    stream_thread = threading.Thread(target=stream_from_queue, args=(client, q))
    stream_thread.daemon = True
    stream_thread.start()

    # Monitor the queue and add more items as needed
    batch_size = 1
    start_index = batch_size
    while start_index < len(songs):
        if q.qsize() < batch_size:
            queue_songs_and_intros(
                q, songs, start_index=start_index, batch_size=batch_size
            )
            start_index += batch_size

    # Wait for the queue to be empty
    q.join()


if __name__ == "__main__":
    main()
