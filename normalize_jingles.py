import os
import subprocess
from config import JINGLES_DIR

def normalize_jingles(input_folder: str):
    # Set a default input folder if none is provided
    if not input_folder:
        input_folder = JINGLES_DIR

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        # Process only .mp3 files
        if filename.endswith(".mp3"):
            input_file = os.path.join(input_folder, filename)

            # FFmpeg command to normalize the audio using EBU R128 loudness standard
            try:
                subprocess.run([
                    'ffmpeg', '-i', input_file,
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-y',  # Overwrite output without asking
                    input_file  # Output is the same as input, so it overwrites
                ], check=True)
                print(f"Normalized: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error normalizing {filename}: {e}")
