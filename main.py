import random
from music_manager import index_music_directory, get_song_metadata
from announcement_generator import (
    generate_start_introduction,
    generate_announcement_text,
)
from tts_generator import generate_tts_audio
from config import INTRO_SONG_PATH, MUSIC_DIR
from logger import log
from liquidsoap_client import LiquidsoapClient
from pathlib import Path
from pydub import AudioSegment

def play_intro_with_fade(intro_text, intro_song_path):
    """Play the introduction with a fade-in effect over the intro song."""
    intro_filename = "combined_intro.mp3"
    file_path = Path(MUSIC_DIR) / intro_filename

    if intro_song_path is None or intro_song_path == "":
        if generate_tts_audio(intro_text, filename=intro_filename):
            log("No intro song path provided. Playing the introduction alone.")
            return str(file_path)
    else:
        intro_audio = AudioSegment.from_file(intro_song_path)
        if generate_tts_audio(intro_text, filename=intro_filename):
            intro_tts_audio = AudioSegment.from_file(file_path)
            combined_audio = intro_tts_audio.overlay(intro_audio, position=0)
            combined_audio.export(file_path, format="mp3")
            return str(file_path)

def create_playlist():
    """Create a playlist from the indexed songs in the music directory."""
    songs = index_music_directory()
    random.shuffle(songs)
    return songs

def queue_songs_and_intros(client, songs, start_index=0, batch_size=5):
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
                tts_path = generate_tts_audio(announcement_text)
                if tts_path:
                    client.queue_song(tts_path, "Announcement - DJ Mašina")
            client.queue_song(song, f"{metadata['title']} - {metadata['artist']}")
            previous_song_metadata = metadata
        else:
            log(f"Skipping song due to missing metadata: {song}")

def main():
    """Main function to run the AI DJ streaming service."""
    log("Creating a new playlist.")
    songs = create_playlist()

    # Generate and play the introduction
    intro_text = generate_start_introduction()
    intro_audio_path = play_intro_with_fade(intro_text, INTRO_SONG_PATH)

    # Connect to Liquidsoap server
    client = LiquidsoapClient()

    # Queue the introduction
    if intro_audio_path:
        client.queue_song(intro_audio_path, "Introduction - DJ Mašina")

    # Queue initial batch of songs and intros
    queue_songs_and_intros(client, songs, start_index=0, batch_size=5)

    # Monitor the queue and add more items as needed
    batch_size = 2
    start_index = batch_size
    while start_index < len(songs):
        queue_songs_and_intros(client, songs, start_index=start_index, batch_size=batch_size)
        start_index += batch_size

if __name__ == "__main__":
    main()