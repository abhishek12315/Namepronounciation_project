import io
import pandas as pd
import numpy as np
import json

student_data = pd.read_excel("./updated_project/Student_info.xlsx")
email_addresses = np.array(student_data.loc[:,"email address"])
umids = np.array(student_data.loc[:,"UMID"])

from qr_code_uploader import QRCodeUploader
# Create an instance of the QRCodeUploader class
qr_uploader = QRCodeUploader()

for umid, email in zip(umids, email_addresses):
    qr_img = qr_uploader.generate_qr_code(umid)

    # Create an in-memory file-like object to store the converted image data
    image_buffer = io.BytesIO()
    qr_img.save(image_buffer, format='JPEG')
    image_data = image_buffer.getvalue()
    
    qr_uploader.send_email(email, image_data)
    
#%%

from audio_processing import Anonymized_audio
from namecoach import namecoachapi
#Create an instance of Anonymized_audio class
audio_processor = Anonymized_audio()
audiofilesaccess = namecoachapi()
# Path to the JSON file
json_file_path = './updated_project/No_Audio_file.json'

# Load existing email addresses from the JSON file
with open(json_file_path, 'r') as file:
    file_content = file.read()
    if file_content:
        No_Audio_file_students = json.loads(file_content)
    else:
        No_Audio_file_students = []

for umid, email in zip(umids, email_addresses):
    output_file = audio_processor.anonymize_umid(umid)
    sound = audiofilesaccess.access_audio_files(email)
    if sound is None:
        if email in No_Audio_file_students:
            print(f"Following student with email address {email} did not uploaded the audio file")
        else: 
            No_Audio_file_students.append(email)
            with open(json_file_path, "w") as file:
                json.dump(No_Audio_file_students, file)  
        continue

    # Store it locally now.
    path_to_store = "./updated_project/Anonymized_audios/"
    audio_processor.upload_audio_locally(output_file, sound, path_to_store)
