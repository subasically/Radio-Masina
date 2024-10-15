import requests

OPENAI_API_KEY = "sk-WW_qh8R1E0CXqvImBRH7Xd_Z2H4veKJ_BGt9bGEDHbT3BlbkFJOgGKIoMKW7n_r6GvLtQtDOBYLkTXkXBEJillAGhO8A"


def generate_announcement(song_title, artist):
    prompt = f"The next song is '{song_title}' by {artist}. Enjoy the music!"
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        },
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error generating announcement: {response.status_code}")
        return None
