import os
from config import OPENAI_API_KEY, INTROS_DIR, DJ_NAME
from logger import log
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1
from announcement_generator import generate_start_introduction

# Initialize OpenAI client
openai = OpenAI(api_key=OPENAI_API_KEY)

def generate_tts_audio(text, filename, voice="nova", model="tts-1"):
    log(f"Generating TTS audio...", "tts_generator")

    """Generate TTS audio from text using OpenAI API."""
    speech_file_path = Path(INTROS_DIR) / filename  # Define output file path as a Path object

    try:
        # Create the TTS audio using OpenAI
        response = openai.audio.speech.create(model=model, voice=voice, input=text)

        # Check if response has valid content
        if response and response.content:
            # Ensure the directory exists
            speech_file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(speech_file_path, "wb") as audio_file:
                audio_file.write(response.content)  # Write the content to file

            # Load the audio file with pydub
            audio = AudioSegment.from_file(speech_file_path)
            # Export the audio as mp3
            audio.export(speech_file_path, format="mp3")

            # Add metadata to the generated TTS audio
            tts_audio = MP3(speech_file_path, ID3=ID3)
            tts_audio["TIT2"] = TIT2(encoding=3, text="Announcement")
            tts_audio["TPE1"] = TPE1(encoding=3, text=DJ_NAME)
            tts_audio.save()

            log(f"Finished generating TTS audio and saved to {speech_file_path}", "tts_generator")
            return str(speech_file_path)  # Return the file path as a string
        else:
            log("No audio content returned in response.", "tts_generator")
            return None

    except Exception as e:
        log(f"Error generating TTS audio: {e}", "tts_generator")
        return None

if __name__ == "__main__":
    # Example usage
    voice = "nova"  # Default voice name
    text_to_speak = generate_start_introduction()  # Generate DJ introduction text
    generate_tts_audio(text_to_speak, "output_example.mp3", voice)