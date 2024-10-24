from pydub import AudioSegment
from pathlib import Path
from logger import log
from tts_generator import generate_tts_audio
from config import INTROS_DIR, DJ_NAME
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1

intro_queued = False  # Initialize the flag

def play_intro_with_fade(intro_text, intro_song_path, output_path=None):
    """Play the introduction with a fade-in effect over the intro song."""
    global intro_queued
    if intro_queued:
        log("Introduction already queued. Skipping.", "main")
        return None
      
    if output_path is None:
        output_path = Path(INTROS_DIR) / "combined_intro.mp3"

    # Generate the TTS audio for the intro
    intro_filename = "ai_dj_intro.mp3"
    intro_file_path = Path(INTROS_DIR) / intro_filename
    if not generate_tts_audio(intro_text, filename=str(intro_file_path)):
        log("Failed to generate TTS audio.", "main")
        return None

    # Load the intro song and the AI DJ intro
    intro_song = AudioSegment.from_file(intro_song_path)
    ai_dj_intro = AudioSegment.from_file(intro_file_path)

    # Define timing and volume variables
    intro_start_offset = 15000  # Start the AI DJ intro 15 seconds into the intro song
    intro_fade_out_duration = 2000  # Duration for fading out the intro song
    intro_fade_in_duration = 2000  # Duration for fading in the intro song
    crossfade_duration = 1000  # Duration for crossfading
    volume_reduction_db = 20  # Volume reduction in dB

    ai_dj_intro_fade_in_duration = 500  # Duration for fading in the AI DJ intro

    # Reduce the volume of the intro song by -20dB during the AI DJ intro
    intro_song_reduced = intro_song - volume_reduction_db
    ai_dj_intro = ai_dj_intro + 10  # Increase the volume of the AI DJ intro by 10dB

    # Apply fade-out to the intro song before the AI DJ intro starts
    intro_song_faded_out = intro_song[:intro_start_offset].fade_out(intro_fade_out_duration)

    # Apply fade-in to the AI DJ intro
    ai_dj_intro_faded_in = ai_dj_intro.fade_in(ai_dj_intro_fade_in_duration)

    # Combine the AI DJ intro with the reduced volume intro song
    combined_audio = intro_song_faded_out + ai_dj_intro_faded_in.overlay(intro_song_reduced[intro_start_offset:], position=0)

    # Fade back in the intro song to its default dB level after the AI DJ intro
    combined_audio = combined_audio.append(intro_song[len(ai_dj_intro) + intro_start_offset:].fade_in(intro_fade_in_duration), crossfade=crossfade_duration)

    # Export the combined audio
    combined_audio_path = Path(output_path)
    combined_audio.export(combined_audio_path, format="mp3")

    # Add metadata to the combined audio
    audio = MP3(combined_audio_path, ID3=ID3)
    audio["TIT2"] = TIT2(encoding=3, text="Introduction")
    audio["TPE1"] = TPE1(encoding=3, text=DJ_NAME)
    audio.save()

    log(f"Combined intro audio saved to: {combined_audio_path}", "main")
    intro_queued = True
    return str(combined_audio_path)

# Example usage
if __name__ == "__main__":
    intro_text = "Zdravo nacija! Dobrodošli na Basic Radio, mjesto gdje se rađaju najbolji zvukovi! Ja sam DJ Mašina, vaša vodičica kroz glazbeni lavirint. Zaboravite na sve brige, jer danas smo tu da se samo smijemo, plešemo i uživamo u muzici. Neka počne ludnica! IDEMO!"
    intro_song_path = "./intros/intro_song.mp3"
    if intro_text and intro_song_path:
        play_intro_with_fade(intro_text, intro_song_path, "./intros/output_intro_example.mp3")