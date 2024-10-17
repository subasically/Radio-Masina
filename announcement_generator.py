# announcement_generator.py

import requests
import random
from config import (
    OPENAI_API_KEY,
    OPENAI_CHAT_API_URL,
    DJ_NAME,
    RADIO_NAME,
    DJ_LANGUAGE,
    DJ_DEMEANOR,
    DJ_GENDER,
)
from logger import log

# Make all announcements based on the following default announcement
DEFAULT_ANNOUNCEMENT = f"Dobrodošli ljubitelji muzike! Ja sam {DJ_NAME}, vaš omiljeni DJ na {RADIO_NAME} radio stanici."

# List of Bosnian sayings for translation
bosniak_sayings = [
    {
        "bosnian": "Ko rano rani, dvije sreće grabi.",
        "english": "The early bird catches two fortunes.",
    },
    {
        "bosnian": "Nije zlato sve što sija.",
        "english": "Not everything that shines is gold.",
    },
    {
        "bosnian": "Bolje spriječiti nego liječiti.",
        "english": "Better to prevent than to cure.",
    },
    {
        "bosnian": "Ko se zadnji smije, najslađe se smije.",
        "english": "He who laughs last, laughs the best.",
    },
    {
        "bosnian": "Što na umu, to na drumu.",
        "english": "What’s on your mind is on the road.",
    },
    {
        "bosnian": "Bolje vrabac u ruci nego golub na grani.",
        "english": "Better a sparrow in the hand than a pigeon on the branch.",
    },
    {
        "bosnian": "Ko tebe kamenom, ti njega hljebom.",
        "english": "If someone throws a stone at you, throw bread back.",
    },
    {
        "bosnian": "Sit gladnom ne vjeruje.",
        "english": "The full don't believe the hungry.",
    },
    {
        "bosnian": "Vuk dlaku mijenja, ali ćud nikada.",
        "english": "The wolf changes its fur, but never its nature.",
    },
    {
        "bosnian": "Puno babica, kilavo dijete.",
        "english": "Too many midwives, a weak child.",
    },
    {"bosnian": "S kim si, takav si.", "english": "You are who you're with."},
    {
        "bosnian": "Kadija te tuži, kadija ti sudi.",
        "english": "The judge accuses you, the judge sentences you.",
    },
    {
        "bosnian": "Pametnom je i išaret dosta.",
        "english": "A wise person needs only a sign.",
    },
    {
        "bosnian": "Nema kruha bez motike.",
        "english": "There’s no bread without a hoe.",
    },
    {
        "bosnian": "Ko nema u glavi, ima u nogama.",
        "english": "He who doesn’t have it in his head, has it in his legs.",
    },
]

random_saying = random.choice(bosniak_sayings)


def generate_announcement_text(
    current_song_title, current_artist, next_song_title, next_artist
):
    """Generate radio DJ announcement text using OpenAI."""
    url = OPENAI_CHAT_API_URL

    # Construct the announcement content conditionally
    announcement_content = (
        f"Generate a {DJ_DEMEANOR} radio DJ announcement for the songs "
    )
    if current_song_title != "" and current_artist != "":
        announcement_content += (
            f"Currently playing: '{current_song_title}' by '{current_artist}'. "
        )
    if next_song_title != "" and next_artist != "":
        announcement_content += (
            f"And next up is '{next_song_title}' by '{next_artist}'. "
        )
    announcement_content += "Enjoy the music!"

    messages = [
        {
            "role": "user",
            "content": f"You are a {DJ_GENDER} AI DJ named '{DJ_NAME}' on '{RADIO_NAME}' radio station.",
        },
        {
            "role": "user",
            "content": "You are in CDT.",
        },
        {"role": "user", "content": "No hashtags or emojis, just plain text."},
        {
            "role": "user",
            "content": announcement_content,
        },
        {
            "role": "user",
            "content": f"Translate the announcement to {DJ_LANGUAGE}.",
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
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        log(f"Error from Chat API: {response.status_code} - {response.text}")
        return None


def generate_start_introduction():
    """Generate radio DJ introduction text using OpenAI."""

    url = OPENAI_CHAT_API_URL
    messages = [
        {
            "role": "user",
            "content": "You are in CDT.",
        },
        {
            "role": "user",
            "content": f"You are {DJ_NAME}, a radio DJ on {RADIO_NAME}, you are a {DJ_GENDER} DJ.",
        },
        {
            "role": "user",
            "content": "No hashtags or emojis, just plain text.",
        },
        {
            "role": "user",
            "content": "Keep the introduction to below 100 words.",
        },
        {
            "role": "user",
            "content": (f"You speak in {DJ_LANGUAGE} language."),
        },
        {
            "role": "user",
            "content": f"Generate a {DJ_DEMEANOR} radio DJ introduction announcement in the following style: {DEFAULT_ANNOUNCEMENT}",
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
        log(f"Introduction: {response.json()['choices'][0]['message']['content']}")
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        log(f"Error from Chat API: {response.status_code} - {response.text}")
        return None
