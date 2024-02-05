from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import pandas as pd

def convert_to_wav(input_file, output_folder):
    audio = AudioSegment.from_file(input_file, format="m4a")
    output_file = os.path.join(output_folder, "converted_audio.wav")
    audio.export(output_file, format="wav")
    return output_file

def cut_audio(input_file, output_folder, silence_threshold=-40):
    # Convert .m4a to .wav
    wav_file = convert_to_wav(input_file, output_folder)

    # Load the converted wav file
    audio = AudioSegment.from_file(wav_file)

    # Split on silence
    chunks = split_on_silence(audio, silence_thresh=silence_threshold)
    student_data = pd.read_excel(os.path.join(os.path.dirname(__file__), "./203-227_audio_files.xlsx"), dtype={"UMID": str}, header=0)
    
    # Export each chunk as a separate file
    for i, chunk in enumerate(chunks):
        name = student_data["Diploma Name"][i]
        umid = student_data["UMID"][i]
        output_file = os.path.join(output_folder, f"{name} {umid}.mp3")
        chunk.export(output_file, format="mp3")

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), "./Fall_2023_Commencement_5of5.m4a")
    output_folder = os.path.join(os.path.dirname(__file__), "../output_chunks1/203_227")

    # Specify silence threshold (in dB). Adjust this value based on your recordings.
    silence_threshold = -40

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    cut_audio(input_file, output_folder, silence_threshold)
# student_data = pd.read_excel(os.path.join(os.path.dirname(__file__), "./51-100_audio_files.xlsx"), dtype={"UMID": str}, header=0)
# print(student_data["UMID"][0])