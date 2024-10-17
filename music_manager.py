import os
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from config import MUSIC_DIR, AUDIO_EXTENSIONS
from logger import log


def index_music_directory():
    """Index the music directory and return a list of available songs."""
    log(f"Indexing music directory: {MUSIC_DIR}")
    songs = []
    for root, _, files in os.walk(MUSIC_DIR):
        for file in files:
            if file.endswith(AUDIO_EXTENSIONS):  # Check for supported audio formats
                songs.append(os.path.join(root, file))
    log(f"Indexed {len(songs)} songs.")
    return songs


def get_song_metadata(song_path):
    """Extract metadata from a song file."""
    log(f"Extracting metadata from: {song_path}")
    extension = os.path.splitext(song_path)[1].lower()

    if extension == ".mp4" or extension == ".m4a":
        audio = MP4(song_path)
        if audio is not None:
            metadata = {
                "title": audio.tags.get("\xa9nam", [None])[0],
                "artist": audio.tags.get("\xa9ART", [None])[0],
                "album": audio.tags.get("\xa9alb", [None])[0],
                "year": audio.tags.get("\xa9day", [None])[0],
            }
            return metadata
        else:
            log(f"Error reading metadata from {song_path}")
            return None

    elif extension == ".mp3":
        try:
            audio = MP3(song_path, ID3=EasyID3)
            metadata = {
                "title": audio.get("title", [None])[0],
                "artist": audio.get("artist", [None])[0],
                "album": audio.get("album", [None])[0],
                "year": audio.get("date", [None])[0],
            }
            return metadata
        except Exception as e:
            log(f"Error reading metadata from {song_path}: {e}")
            return None

    else:
        log(f"Unsupported file format: {song_path}")
        return None


# Example usage
if __name__ == "__main__":
    import random

    # Index the music directory
    songs = index_music_directory()

    # Get metadata for the first song in the list
    if songs:
        random_song = songs[random.randint(0, len(songs) - 1)]
        fixed_song = "./music/Mirko Plavsic - Manastir.m4a"
        song = fixed_song
        metadata = get_song_metadata(song)
        if metadata:
            print(f"Metadata for {song}:")
            print(f"Title: {metadata['title']}")
            print(f"Artist: {metadata['artist']}")
            print(f"Album: {metadata['album']}")
            print(f"Year: {metadata['year']}")
        else:
            print(f"Failed to extract metadata for {song}")
    else:
        print("No songs found in the music directory.")
