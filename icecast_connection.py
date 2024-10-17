# icecast_connection.py

import shout
from config import (
    ICECAST_HOST,
    ICECAST_PORT,
    ICECAST_USER,
    ICECAST_PASSWORD,
    ICECAST_MOUNT,
    ICECAST_FORMAT,
    ICECAST_BITRATE,
    ICECAST_SAMPLERATE,
    ICECAST_CHANNELS,
)
from logger import log


def connect_to_icecast():
    """Connect to the Icecast server."""
    client = shout.Shout()
    client.host = ICECAST_HOST
    client.port = ICECAST_PORT
    client.user = ICECAST_USER
    client.password = ICECAST_PASSWORD
    client.mount = ICECAST_MOUNT
    client.format = ICECAST_FORMAT
    client.protocol = "http"
    client.public = 1
    client.audio_info = {
        shout.SHOUT_AI_BITRATE: ICECAST_BITRATE,
        shout.SHOUT_AI_SAMPLERATE: ICECAST_SAMPLERATE,
        shout.SHOUT_AI_CHANNELS: ICECAST_CHANNELS,
    }
    log("Connecting to Icecast server.")
    try:
        client.open()  # Use the open() method to connect
        client.get_connected()
        log("Connected to Icecast server.")
    except shout.ShoutException as e:
        log(f"Could not connect to Icecast server: {e}")
        return None
    return client
