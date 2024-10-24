# announcement_generator.py

import requests
import random
import time
from config import (
    OPENAI_API_KEY,
    OPENAI_CHAT_API_URL,
    DJ_NAME,
    RADIO_NAME,
    DJ_LANGUAGE,
    DJ_GENDER,
    DJ_DEMEANOR
)
from logger import log

CURRENT_TIME = time.strftime("%H:%M")

# Make all announcements based on the following default announcement
# DEFAULT_ANNOUNCEMENT = f"Cao, ljudi! Ja sam {DJ_NAME}, vaš DJ na {RADIO_NAME} radio. Spremite se za naj bolju muziku! Držite se tu, jer samo najbolje svira sada!"

# List of Bosnian sayings for translation
bosniak_sayings = [
    {"bosnian": "Nije zlato sve što sija."},
    {"bosnian": "S kim si, takav si."},
    {"bosnian": "Nema kruha bez motike."},
    {"bosnian": "Ko nema u glavi, ima u nogama."},
]

random_saying = random.choice(bosniak_sayings)

def generate_announcement_text(
    current_song_title, current_artist, next_song_title, next_artist
):
    """Generate radio DJ announcement text using OpenAI."""
    url = OPENAI_CHAT_API_URL

    # Construct the announcement content conditionally
    announcement_content = f"Hej raja, pozdrav iz studija! upravo smo čuli '{current_song_title}' od '{current_artist}'. "
    if next_song_title != "" and next_artist != "":
        announcement_content += (
            f"a sad ide '{next_song_title}' od '{next_artist}'. "
        )

    messages = [
        {
            "role": "user",
            "content": f"It is {CURRENT_TIME}.",
        },
        {
            "role": "user",
            "content": f"You are a DJ named '{DJ_NAME}' on '{RADIO_NAME}' radio station, you are a{DJ_GENDER}, and love playing Balkan/Narodna music.",
        },
        {
            "role": "user",
            "content": "Mention the time of day(morning, afternoon, evening) like you're chatting with friends.",
        },
        {"role": "user", "content": "No hashtags or emojis, just plain text."},
        {
            "role": "user",
            "content": f"Generate an announcement in the following style: {announcement_content}",
        },
        {
            "role": "user",
            "content": f"Speak in {DJ_LANGUAGE}.",
        },
    ]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url, headers=headers, json={"model": "gpt-3.5-turbo", "messages": messages}
    )

    if response.status_code == 200:
        log(f"Announcement generated,", "announcement_generator")
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        log(f"Error from Chat API: {response.status_code} - {response.text}", "announcement_generator")
        return None


def generate_start_introduction(previous_intro=""):
    """Generate radio DJ introduction text using OpenAI."""

    url = OPENAI_CHAT_API_URL
    messages = [
        {
            "role": "user",
            "content": f"It is {CURRENT_TIME}.",
        },
        {
            "role": "user",
            "content": "Mention the time of day(morning, afternoon, evening) like you're chatting with friends.",
        },
        {
            "role": "user",
            "content": f"You are {DJ_NAME} and you are a {DJ_GENDER},  and you love sharing Balkan songs with the listeners.",
        },
        {
            "role": "user",
            "content": "No hashtags or emojis, keep it cool and informal.",
        },
        {
            "role": "user",
            "content": f"You speak in {DJ_LANGUAGE} and have a {DJ_DEMEANOR} demeanor.",
        },
        {
            "role": "user",
            "content": "Keep it to 200 words or less.",
        },
        {
            "role": "user",
            "content": f"Generate a chill and laid-back intro to the start of your live stream.",
        },
    ]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url, headers=headers, json={"model": "gpt-3.5-turbo", "messages": messages}
    )

    if response.status_code == 200:
        log(f"Introduction generated.", "announcement_generator")
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        log(f"Error from Chat API: {response.status_code} - {response.text}", "announcement_generator")
        return None


if __name__ == "__main__":
    # Example usage
    current_song_title = "Supermen"
    current_artist = "Dino Merlin"
    next_song_title = "Kuda idu ljudi kao ja"
    next_artist = "Aca Lukas"
    announcement_text = generate_announcement_text(
        current_song_title, current_artist, next_song_title, next_artist
    )
    start_introduction = generate_start_introduction()