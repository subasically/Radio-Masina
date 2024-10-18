import requests
from config import LIQUIDSOAP_HOST, LIQUIDSOAP_PORT
from logger import log


class LiquidsoapClient:
    def __init__(self, host=LIQUIDSOAP_HOST, port=LIQUIDSOAP_PORT):
        self.host = host
        self.port = port

    def queue_song(self, song_path, title=None):
        url = f"http://{self.host}:{self.port}/play?file={song_path}"
        if title:
            url += f"&title={title}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                log(f"Successfully queued song: {title if title else song_path}")
                return response.text
            else:
                log(
                    f"Failed to queue song: {title if title else song_path}. Status code: {response.status_code}"
                )
                return None
        except Exception as e:
            log(f"Error queuing song: {e}")
            return None
