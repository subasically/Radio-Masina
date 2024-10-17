from pydub import AudioSegment
from pydub.playback import play
from liquidsoap_client import LiquidsoapClient
from logger import log
import tempfile


def play_song(client, song, title, artist):
    """Queue the specified song on the Liquidsoap server."""
    log(f"Queuing song: {title} by {artist}")
    try:
        if isinstance(song, AudioSegment):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                song.export(tmp_file.name, format="mp3")
                song_path = tmp_file.name
        else:
            song_path = song

        response = client.queue_song(song_path)
        log(f"Liquidsoap response: {response}")

    except Exception as e:
        log(f"Error queuing song: {e}")
