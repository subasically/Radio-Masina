import os
import subprocess

def convert_m4a_to_mp3(input_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".m4a"):
                input_file = os.path.join(root, file)
                output_file = os.path.splitext(input_file)[0] + ".mp3"
                command = [
                    "ffmpeg",
                    "-i", input_file,
                    "-codec:a", "libmp3lame",
                    "-qscale:a", "2",
                    "-map_metadata", "0",
                    output_file
                ]
                subprocess.run(command, check=True)
                print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    input_directory = "./music"  # Change this to your directory containing .m4a files
    convert_m4a_to_mp3(input_directory)