import os
from pydub import AudioSegment

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# Set input and output directories
input_directory = r"Audio_files"
output_directory = os.path.join(input_directory, "Normalized_audio")

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Process each MP3 file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".mp3"):
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(output_directory, filename)
        
        # Load the audio
        sound = AudioSegment.from_file(input_file, format="mp3")
        
        # Normalize the audio
        normalized_sound = match_target_amplitude(sound, -20.0)
        
        # Export the normalized audio
        normalized_sound.export(output_file, format="mp3")

