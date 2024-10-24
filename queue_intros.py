# queue_intros.py

from announcement_generator import generate_announcement_text
from tts_generator import generate_tts_audio
from normalize_audio import normalize_audio
from logger import log
from liquidsoap_client import LiquidsoapClient

def queue_intros(client, previous_song_metadata, current_song_metadata):
    """Queue intros and announcements using LiquidsoapClient."""
    if previous_song_metadata:
        announcement_text = generate_announcement_text(
            previous_song_metadata["title"],
            previous_song_metadata["artist"],
            current_song_metadata["title"],
            current_song_metadata["artist"],
        )
        log(f"Announcement: {announcement_text}", "queue_intros")
        tts_path = generate_tts_audio(announcement_text, filename="announcement.mp3")
        normalize_audio(tts_path)
        if tts_path:
            client.queue_song(tts_path, "Announcement - DJ Mašina", queue="playImmediate")