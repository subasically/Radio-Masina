# config.py

import os
from logger import log

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
ICECAST_HOST = os.getenv("ICECAST_HOST", "icecast")
ICECAST_PORT = int(os.getenv("ICECAST_PORT", 8000))
ICECAST_USER = os.getenv("ICECAST_USER", "admin")
ICECAST_PASSWORD = os.getenv("ICECAST_PASSWORD", "hackme")
ICECAST_MOUNT = os.getenv("ICECAST_MOUNT", "radio")
ICECAST_FORMAT = os.getenv("ICECAST_FORMAT", "mp3")
ICECAST_BITRATE = int(os.getenv("ICECAST_BITRATE", 192))
ICECAST_SAMPLERATE = int(os.getenv("ICECAST_SAMPLERATE", 44100))
ICECAST_CHANNELS = int(os.getenv("ICECAST_CHANNELS", 2))
LIQUIDSOAP_HOST = os.getenv("LIQUIDSOAP_HOST", "localhost")
LIQUIDSOAP_PORT = int(os.getenv("LIQUIDSOAP_PORT", 7001))
MUSIC_DIR = os.getenv(
    "MUSIC_DIR",
    "./music",
)
JINGLES_DIR = os.getenv("JINGLES_DIR", "./jingles")
INTROS_DIR = os.getenv("INTROS_DIR", "./intros")
DJ_NAME = os.getenv("DJ_NAME", "DJ Mašina")
DJ_GENDER = os.getenv("DJ_GENDER", "Female")
DJ_DEMEANOR = os.getenv("DJ_DEMEANOR", "Fun and Energetic")
DJ_LANGUAGE = os.getenv("DJ_LANGUAGE", "Bosnian")
AUDIO_EXTENSIONS = tuple(
    os.getenv("AUDIO_EXTENSIONS", ".mp3,.m4a,.wav,.flac").split(",")
)

# Log the configuration settings
log("*" * 80)
log("Configuration settings:", "config")
log(f"RADIO_NAME: {RADIO_NAME}", "config")
log(f"OPENAI_API_KEY: {OPENAI_API_KEY}", "config")
log(f"OPENAI_CHAT_API_URL: {OPENAI_CHAT_API_URL}", "config")
log(f"OPENAI_TTS_API_URL: {OPENAI_TTS_API_URL}", "config")
log(f"OPENAI_VOICE: {OPENAI_VOICE}", "config")
log(f"ICECAST_HOST: {ICECAST_HOST}", "config")
log(f"ICECAST_PORT: {ICECAST_PORT}", "config")
log(f"ICECAST_USER: {ICECAST_USER}", "config")
log(f"ICECAST_PASSWORD: {ICECAST_PASSWORD}", "config")
log(f"ICECAST_MOUNT: {ICECAST_MOUNT}", "config")
log(f"ICECAST_FORMAT: {ICECAST_FORMAT}", "config")
log(f"ICECAST_BITRATE: {ICECAST_BITRATE}", "config")
log(f"ICECAST_SAMPLERATE: {ICECAST_SAMPLERATE}", "config")
log(f"ICECAST_CHANNELS: {ICECAST_CHANNELS}", "config")
log(f"LIQUIDSOAP_HOST: {LIQUIDSOAP_HOST}", "config")
log(f"LIQUIDSOAP_PORT: {LIQUIDSOAP_PORT}", "config")
log(f"MUSIC_DIR: {MUSIC_DIR}", "config")
log(f"JINGLES_DIR: {JINGLES_DIR}", "config")
log(f"INTROS_DIR: {INTROS_DIR}", "config")
log(f"DJ_NAME: {DJ_NAME}", "config")
log(f"DJ_DEMEANOR: {DJ_DEMEANOR}", "config")
log(f"DJ_LANGUAGE: {DJ_LANGUAGE}", "config")
log(f"AUDIO_EXTENSIONS: {AUDIO_EXTENSIONS}", "config")
log("Configuration settings end.", "config")
log("*" * 80)