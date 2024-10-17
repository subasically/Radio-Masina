# config.py

import os

# Hardcoded values (to be replaced with environment variables later)
OPENAI_API_KEY = "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"
OPENAI_CHAT_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TTS_API_URL = "https://api.openai.com/v1/audio/speech"
ICECAST_HOST = "10.10.10.5"
ICECAST_PORT = 8005
ICECAST_USER = "AI_RADIO_MASINA"
ICECAST_PASSWORD = "Fildo198&"
ICECAST_MOUNT = "/"
ICECAST_FORMAT = "mp3"
ICECAST_BITRATE = "192"
ICECAST_SAMPLERATE = "44100"
ICECAST_CHANNELS = "2"
LIQUIDSOAP_HOST = "10.10.10.5"
LIQUIDSOAP_PORT = 8000
RADIO_NAME = "Basic Radio"
DJ_NAME = "DJ Mašina"
MUSIC_DIR = "./music"
INTRO_SONG_PATH = "./intro_song.mp3"  # ./intro_song.mp3
DJ_DEMEANOR = "Fun and Energetic"
DJ_GENDER = "Female"

# Supported audio file extensions
AUDIO_EXTENSIONS = (".mp3", ".m4a", ".wav", ".flac")

# New variables
DJ_LANGUAGE = "Bosnian"  # Default spoken language
OPENAI_VOICE = "nova"  # Default OpenAI voice name
