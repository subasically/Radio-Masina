import random
from music_manager import index_music_directory, get_song_metadata
from announcement_generator import (
    generate_start_introduction,
    generate_announcement_text,
)
from tts_generator import generate_tts_audio
from config import INTROS_DIR
from logger import log
from liquidsoap_client import LiquidsoapClient
from pathlib import Path
from pydub import AudioSegment

intro_queued = False  # Initialize the flag

def play_intro_with_fade(intro_text, INTROS_DIR):
    """Play the introduction with a fade-in effect over the intro song."""
    global intro_queued
    if intro_queued:
        log("Introduction already queued. Skipping.", "main")
        return None

    if INTROS_DIR is None or INTROS_DIR == "":
        intro_filename = "intro_song.mp3"
    else:
        intro_filename = "ai_dj_intro_song.mp3"
    
    file_path = Path(INTROS_DIR) / intro_filename if INTROS_DIR else Path(intro_filename)

    log(f"Intro file path: {file_path}", "main")

    if INTROS_DIR is None or INTROS_DIR == "":
        if generate_tts_audio(intro_text, filename=str(file_path)):
            log("No intro song path provided. Playing the introduction alone.", "main")
            intro_queued = True
            return str(file_path)
    else:
        intro_song_path = Path(INTROS_DIR) / "intro_song.mp3"  # Specify the actual intro song file
        if not intro_song_path.exists():
            log(f"Intro song file does not exist: {intro_song_path}", "main")
            return None

        intro_audio = AudioSegment.from_file(intro_song_path)
        if generate_tts_audio(intro_text, filename=str(file_path)):
            intro_tts_audio = AudioSegment.from_file(file_path)
            combined_audio = intro_tts_audio.overlay(intro_audio, position=0)
            combined_audio.export(file_path, format="mp3")
            log(f"Combined intro audio saved to: {file_path}", "main")
            intro_queued = True
            return str(file_path)
        else:
            log("Failed to generate TTS audio.", "main")
            return None

def create_playlist():
    """Create a playlist from the indexed songs in the music directory."""
    songs = index_music_directory()
    random.shuffle(songs)
    return songs

def queue_songs_and_intros(client, songs, start_index=0, batch_size=1):
    """Queue a batch of songs and their intros using LiquidsoapClient."""
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
                tts_path = generate_tts_audio(announcement_text, filename="announcement.mp3")
                if tts_path:
                    client.queue_song(tts_path, "Announcement - DJ Mašina", queue="intro")
            client.queue_song(song, f"{metadata['title']} - {metadata['artist']}", queue="play")
            previous_song_metadata = metadata
        else:
            log(f"Skipping song due to missing metadata: {song}", "main")

def main():
    """Main function to run the AI DJ streaming service."""
    log("Creating a new playlist.", "main")
    
    # Generate and play the introduction
    intro_text = generate_start_introduction()
    intro_audio_path = play_intro_with_fade(intro_text, INTROS_DIR)

    # Connect to Liquidsoap server
    client = LiquidsoapClient()

    # Queue the introduction
    if not intro_queued:
        client.queue_song(intro_audio_path, "Introduction - DJ Mašina", queue="intro")
    else:
        log("Introduction already queued. Skipping.", "main")
        log("Starting the playlist...", "main")

        # Comment out the song queuing part for now
        songs = create_playlist()
        queue_songs_and_intros(client, songs, start_index=0, batch_size=1)

        # Monitor the queue and add more items as needed
        batch_size = 1
        start_index = batch_size
        while start_index < len(songs):
            queue_songs_and_intros(client, songs, start_index=start_index, batch_size=batch_size)
            start_index += batch_size

if __name__ == "__main__":
    main()