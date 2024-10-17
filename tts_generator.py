# tts_generator.py

from config import OPENAI_API_KEY
from logger import log
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment  # Import pydub for audio manipulation

# Initialize OpenAI client
openai = OpenAI(api_key=OPENAI_API_KEY)


def generate_tts_audio(text, filename, voice="nova", model="tts-1"):
    log(f"Generating TTS audio...")

    """Generate TTS audio from text using OpenAI API."""
    speech_file_path = Path(filename)  # Define output file path

    try:
        # Create the TTS audio using OpenAI
        response = openai.audio.speech.create(model=model, voice=voice, input=text)

        # Check if response has valid content
        if response and response.content:
            with open(speech_file_path, "wb") as audio_file:
                audio_file.write(response.content)  # Write the content to file

            # Increase the volume of the generated audio
            audio = AudioSegment.from_file(speech_file_path)
            louder_audio = audio.apply_gain(12)  # Increase volume by 12dB

            # Export the modified audio
            louder_audio.export(speech_file_path, format="mp3")

            log(f"Finished generating TTS audio and saved to {filename}")
            return True
        else:
            log("No audio content returned in response.")
            return False

    except Exception as e:
        log(f"Error generating TTS audio: {e}")
        return False


if __name__ == "__main__":
    # Example usage
    voice = "nova"  # Default voice name
    text_to_speak = "Zdravo nacija! Dobrodošli na Basic Radio, mjesto gdje se rađaju najbolji zvukovi! Ja sam DJ Mašina, vaša vodičica kroz glazbeni lavirint. Zaboravite na sve brige, jer danas smo tu da se samo smijemo, plešemo i uživamo u muzici. Neka počne ludnica! IDEMO!"
    filename = f"introduction_example_{voice}.mp3"  # Change as needed
    generate_tts_audio(text_to_speak, filename, voice)
