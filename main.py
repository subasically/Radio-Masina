import random
from music_manager import index_music_directory, get_song_metadata
from announcement_generator import generate_start_introduction
from config import INTROS_DIR, JINGLES_DIR
from logger import log
from liquidsoap_client import LiquidsoapClient
from pathlib import Path
from audio_mixer import play_intro_with_fade  # Ensure this import is correct
from queue_songs import queue_songs
from queue_intros import queue_intros

intro_queued = False  # Initialize the flag

def create_playlist():
    """Create a playlist from the indexed songs in the music directory."""
    log("Creating a new playlist.", "main")
    songs = index_music_directory()
    random.shuffle(songs)
    return songs

def main():
    """Main function to run the AI DJ streaming service."""
    log("Starting the AI DJ streaming service...", "main")
    
    # Normalize the jingles
    # normalize_audio(JINGLES_DIR)
    
    # Generate and play the introduction
    intro_text = generate_start_introduction()
    if intro_text is None:
        log("Failed to generate AI DJ introduction. Using default introduction.", "main")
        intro_audio_path = Path(INTROS_DIR) / "DEFAULT_DJ_INTRO.mp3"
    else:
        intro_audio_path = play_intro_with_fade(intro_text, Path(INTROS_DIR) / "intro_song.mp3")

    # Connect to Liquidsoap server
    client = LiquidsoapClient(queue="play")

    # Queue the introduction
    if not intro_queued:
        client.queue_song(str(intro_audio_path), "Introduction - DJ Mašina", queue="playImmediate")
    else:
        log("Introduction already queued. Skipping.", "main")
    #     log("Starting the playlist...", "main")

    #     # Create the playlist
    #     songs = create_playlist()

    #     # Queue songs and intros
    #     previous_song_metadata = None
    #     for i in range(len(songs)):
    #         song = songs[i]
    #         metadata = get_song_metadata(song)
    #         if metadata:
    #             queue_intros(client, previous_song_metadata, metadata)
    #             queue_songs(client, [song], start_index=0, batch_size=3)
    #             previous_song_metadata = metadata
    #         else:
    #             log(f"Skipping song due to missing metadata: {song}", "main")

    # log("AI DJ streaming service started successfully.", "main")

    # Keep the script running
    log("AI DJ streaming service initialization complete. Press Ctrl+C to exit.", "main")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        log("AI DJ streaming service terminated.", "main")

if __name__ == "__main__":
    log("Initializing the AI DJ streaming service...", "main")
    main()
    log("AI DJ streaming service initialization complete.", "main")