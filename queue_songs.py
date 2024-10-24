# queue_songs.py

from music_manager import get_song_metadata
from logger import log
from liquidsoap_client import LiquidsoapClient

def queue_songs(client, songs, start_index=0, batch_size=1):
    """Queue a batch of songs using LiquidsoapClient."""
    for i in range(start_index, min(start_index + batch_size, len(songs))):
        song = songs[i]
        metadata = get_song_metadata(song)
        if metadata:
            client.queue_song(song, f"{metadata['title']} - {metadata['artist']}", queue="play")
        else:
            log(f"Skipping song due to missing metadata: {song}", "queue_songs")