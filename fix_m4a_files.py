import os
import subprocess

def process_audio_files(input_folder, output_folder):
    print(f"Processing files in {input_folder}")
    # Ensure the output directory exists, create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file has a .m4a extension
        if filename.endswith(".mp3"):
            # Build full input and output file paths
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.mp3")
            
            # Run the ffmpeg command to re-encode or copy the file
            try:
                subprocess.run(['ffmpeg', '-i', input_file, '-c', 'copy', output_file], check=True)
                print(f"Processed: {filename} -> {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e}")

# Example usage
input_folder = "./music"  # The folder containing the .m4a files
output_folder = "./music_fixed"         # The folder where fixed files will be stored
process_audio_files(input_folder, output_folder)
