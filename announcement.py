import requests
import os
import json

OPENAI_API_KEY = "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"


# Function to generate announcement text using OpenAI Chat API
def generate_announcement_text(
    current_song_title, current_artist, next_song_title, next_artist
):
    url = "https://api.openai.com/v1/chat/completions"

    # Prepare the messages for the chat completion request
    messages = [
        {
            "role": "user",
            "content": f"Stvori zabavnu najavu za radio koja jednostavno navodi da trenutno sviramo '{current_song_title}' od '{current_artist}', a slijedeća pjesma je '{next_song_title}' od '{next_artist}'. Ne koristite nikakve emotikone ili heštegove.",
        }
    ]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    # Send request to the Chat API
    response = requests.post(
        url, headers=headers, json={"model": "gpt-3.5-turbo", "messages": messages}
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"][
            "content"
        ].strip()  # Extract and return the generated text
    else:
        print(f"Error from Chat API: {response.status_code} - {response.text}")
        return None


# Your existing TTS function for generating audio files
def generate_tts(text, voice="alloy"):
    url = "https://api.openai.com/v1/audio/speech"

    # Prepare the payload for the TTS API
    payload = json.dumps({"model": "tts-1", "input": text, "voice": voice})

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",  # Correct authorization
        "Content-Type": "application/json",
    }

    # Make the request to the TTS API
    response = requests.post(url, headers=headers, data=payload)

    # Debugging response
    if response.status_code == 200:
        return response.content  # Directly return the audio content
    else:
        print(f"Error from TTS API: {response.status_code} - {response.text}")
        return None


AZURACAST_API_URL = "http://basic-radio.subasically.me/api/nowplaying/1"


def get_current_track():
    headers = {
        "Accept": "application/json",
    }
    response = requests.get(AZURACAST_API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        now_playing = data.get("now_playing")
        playing_next = data.get("playing_next")

        return now_playing, playing_next
    else:
        print(f"Error fetching track: {response.status_code}")
        return None, None


# Main function to run
def main():
    now_playing, playing_next = get_current_track()
    if now_playing and playing_next:
        current_song_title = now_playing["song"]["title"]
        current_artist = now_playing["song"]["artist"]

        next_song_title = playing_next["song"]["title"]
        next_artist = playing_next["song"]["artist"]

        # Generate announcement text using OpenAI
        announcement_text = generate_announcement_text(
            current_song_title, current_artist, next_song_title, next_artist
        )
        if announcement_text:
            print(f"Generated announcement: {announcement_text}")
            voice = "nova"
            audio_data = generate_tts(announcement_text, voice)
            if audio_data:
                audio_file_path = (
                    f"./announcement_{voice}.wav"  # Change this path if needed
                )
                with open(audio_file_path, "wb") as f:
                    f.write(audio_data)
                print(
                    f"Announcement saved as: {audio_file_path}"
                )  # Inform where it's saved
            else:
                print("Failed to generate audio data.")
        else:
            print("Failed to generate announcement text.")
    else:
        print("No current track information available.")


if __name__ == "__main__":
    main()
