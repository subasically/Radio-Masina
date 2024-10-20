import requests
from config import LIQUIDSOAP_HOST, LIQUIDSOAP_PORT
from logger import log


class LiquidsoapClient:
    def __init__(self, host=LIQUIDSOAP_HOST, port=LIQUIDSOAP_PORT, queue=None):
        self.host = host
        self.port = port
        self.queue = queue

    def queue_song(self, song_path, title=None, queue=None):
        url = f"http://{self.host}:{self.port}/{queue}?file={song_path}"
        if title:
            url += f"&title={title}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                log(f"Successfully queued song: {title if title else song_path}", "liquidsoap_client")
                return response.text
            else:
                log(
                    f"Failed to queue song: {title if title else song_path}. Status code: {response.status_code}",
                    "liquidsoap_client"
                )
                return None
        except Exception as e:
            log(f"Error queuing song: {e}", "liquidsoap_client")
            return None
