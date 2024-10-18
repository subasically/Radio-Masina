# config.py

import os

RADIO_NAME = os.getenv("RADIO_NAME", "Basic Radio")
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    "",
)
OPENAI_CHAT_API_URL = os.getenv(
    "OPENAI_CHAT_API_URL", "https://api.openai.com/v1/chat/completions"
)
OPENAI_TTS_API_URL = os.getenv(
    "OPENAI_TTS_API_URL", "https://api.openai.com/v1/audio/speech"
)
OPENAI_VOICE = os.getenv("OPENAI_VOICE", "nova")
ICECAST_HOST = os.getenv("ICECAST_HOST", "10.10.10.5")
ICECAST_PORT = int(os.getenv("ICECAST_PORT", 8000))
ICECAST_USER = os.getenv("ICECAST_USER", "AI_RADIO_MASINA")
ICECAST_PASSWORD = os.getenv("ICECAST_PASSWORD", "Fildo198&")
ICECAST_MOUNT = os.getenv("ICECAST_MOUNT", "/")
ICECAST_FORMAT = os.getenv("ICECAST_FORMAT", "mp3")
ICECAST_BITRATE = int(os.getenv("ICECAST_BITRATE", 192))
ICECAST_SAMPLERATE = int(os.getenv("ICECAST_SAMPLERATE", 44100))
ICECAST_CHANNELS = int(os.getenv("ICECAST_CHANNELS", 2))
LIQUIDSOAP_HOST = os.getenv("LIQUIDSOAP_HOST", "localhost")
LIQUIDSOAP_PORT = int(os.getenv("LIQUIDSOAP_PORT", 7001))
MUSIC_DIR = os.getenv(
    "MUSIC_DIR",
    "",
)
INTRO_SONG_PATH = os.getenv("INTRO_SONG_PATH", "./intro_song.mp3")
DJ_NAME = os.getenv("DJ_NAME", "DJ Mašina")
DJ_GENDER = os.getenv("DJ_GENDER", "Female")
DJ_DEMEANOR = os.getenv("DJ_DEMEANOR", "Fun and Energetic")
DJ_LANGUAGE = os.getenv("DJ_LANGUAGE", "Bosnian")
AUDIO_EXTENSIONS = tuple(
    os.getenv("AUDIO_EXTENSIONS", ".mp3,.m4a,.wav,.flac").split(",")
)
