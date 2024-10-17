import telnetlib
from config import LIQUIDSOAP_HOST, LIQUIDSOAP_PORT
from logger import log


class LiquidsoapClient:
    def __init__(self, host=LIQUIDSOAP_HOST, port=LIQUIDSOAP_PORT):
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = telnetlib.Telnet(self.host, self.port)
            log("Connected to Liquidsoap server.")
        except Exception as e:
            log(f"Failed to connect to Liquidsoap server: {e}")

    def send_command(self, command):
        if self.connection is None:
            self.connect()
        try:
            self.connection.write(command.encode("utf-8") + b"\n")
            response = self.connection.read_until(b"\n").decode("utf-8")
            return response
        except (BrokenPipeError, EOFError) as e:
            log(f"Connection lost: {e}. Reconnecting...")
            self.connect()
            self.connection.write(command.encode("utf-8") + b"\n")
            response = self.connection.read_until(b"\n").decode("utf-8")
            return response
        except Exception as e:
            log(f"Error sending command: {e}")
            return None

    def queue_song(self, song_path):
        command = f'request.push "{song_path}"'
        return self.send_command(command)

    def close(self):
        if self.connection:
            self.connection.close()
