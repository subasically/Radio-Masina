import requests
import sys
import json


def generate_tts(text, language="bs-BA"):
    # Configure your API endpoint and key
    url = "https://api.openai.com/v1/transformers/tts"  # Hypothetical endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with your API key
    }
    body = {"text": text, "voice": language}

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        # Assuming the response contains a URL to the audio file
        audio_url = response.json().get("url")
        audio_response = requests.get(audio_url)
        if audio_response.status_code == 200:
            return audio_response.content
    return None


if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "Nema naslova"
    artist = sys.argv[2] if len(sys.argv) > 2 else "Nema izvođača"
    text = f"Sada slušate {title} od {artist}"
    audio_data = generate_tts(text)
    if audio_data:
        # Assuming you want to save the audio as a WAV file
        with open("/tmp/announcement.wav", "wb") as f:
            f.write(audio_data)
