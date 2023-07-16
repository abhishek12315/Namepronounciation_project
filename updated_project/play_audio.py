import pygame
import os

# Folder path containing audio recordings
folder_path = "./updated_project/Anonymized_audios/"

def play_audio_files(folder_path):
    # Initialize pygame
    pygame.mixer.init()

    # Get a list of all audio files in the folder
    audio_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]

    # Iterate over the audio files
    for audio_file in audio_files:
        file_path = os.path.join(folder_path, audio_file)
        print("Playing:", audio_file)

        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Wait until the audio has finished playing
        while pygame.mixer.music.get_busy():
            continue

    # Quit pygame
    pygame.mixer.quit()

# Call the function to play the audio files
play_audio_files(folder_path)

