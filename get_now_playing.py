import requests
import json

AZURACAST_API_URL = "http://basic-radio.subasically.me/api/nowplaying/1"


def get_current_track():
    headers = {
        "Accept": "application/json",
    }

    response = requests.get(AZURACAST_API_URL, headers=headers)

    if response.status_code == 200:
        return response.json().get("now_playing")
    else:
        print(f"Error fetching track: {response.status_code}")
        return None


# Example usage
current_track = get_current_track()
if current_track:
    print(current_track)
