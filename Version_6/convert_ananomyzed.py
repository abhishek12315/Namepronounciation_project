import pandas as pd
import numpy as np
import os
from Utils_classes.audio_processing import Anonymized_audio
from pydub import AudioSegment
import time

audio_processor = Anonymized_audio()

student_data = pd.read_excel(os.path.join(os.path.dirname(__file__), "./JSONs/Student_info.xlsx"), dtype={"UMID": str}, header=0)

student_data.dropna(subset=["Email", "UMID"], inplace=True)
umids = np.array(student_data.loc[:, "UMID"])

# Folder path containing audio recordings
recording_path = os.path.join(os.path.dirname(__file__), "../Audio_split/Final_Audio")
Anonymized_path = os.path.join(os.path.dirname(__file__), "../Audio_split/Final_Anonymized")
issuess = []
audio_files = [file for file in os.listdir(recording_path) if file.endswith(".mp3")]
count = 0
for umid, audio_file in zip(umids, audio_files):
    output_file = audio_processor.simple_encrypt(umid)
    final_recording_path = os.path.join(recording_path, audio_file)  # Use os.path.join for path concatenation
    if not os.path.exists(final_recording_path):
        print(f"The file '{final_recording_path}' does not exist.")
        continue
    print(umid)
    print(final_recording_path)
    try:
        sound = AudioSegment.from_file(final_recording_path)
        time.sleep(1)
    except:
        issuess.append(umid)
        continue
    
    audio_processor.upload_audio_locally(output_file, sound, Anonymized_path)
    count += 1

print(count)
print(issuess)