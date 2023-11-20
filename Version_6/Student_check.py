from Utils_classes.namecoach import namecoachapi
from Utils_classes.audio_processing import Anonymized_audio
from Utils_classes.email_qrcode import QRCodeUploader
import io
import pandas as pd
import numpy as np
import json
import os
import time
import requests
from pydub import AudioSegment

# Create an instance of the QRCodeUploader class
qr_uploader = QRCodeUploader()

# Create an instance of Anonymized_audio class
audio_processor = Anonymized_audio()
audiofilesaccess = namecoachapi()

student_data = pd.read_excel(os.path.join(os.path.dirname(__file__), "./JSONs/Student_info.xlsx"), dtype={"UMID": str}, header=0)
# student_data = pd.read_excel(os.path.join(os.path.dirname(__file__), "./JSONs/graduate_students_1.xlsx"), dtype={"UMID": str}, header=0, skipfooter=1)

student_data.dropna(subset=["Email", "UMID"], inplace=True)
email_addresses = np.array(student_data.loc[:, "Email"])
umids = np.array(student_data.loc[:, "UMID"])

# Path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), "./JSONs/No_Audio_file.json")

# Load existing email addresses from the JSON file
with open(json_file_path, 'r') as file:
    file_content = file.read()
    if file_content:
        No_Audio_file_students = json.loads(file_content)
    else:
        No_Audio_file_students = []

# Initialize an empty list to store data
data_list = []
count = 0
notdone = 0
for umid, email in zip(umids, email_addresses): 
    recording_link = audiofilesaccess.access_audio_files(email)
    time.sleep(1)
    if recording_link is None:
        if email in No_Audio_file_students:
            print(
                f"Following student with email address {email} did not uploaded the audio file")
        else:
            No_Audio_file_students.append(email)
            with open(json_file_path, "w") as file:
                json.dump(No_Audio_file_students, file)
        continue
    else:
        output_file = audio_processor.simple_encrypt(umid)
        # Locate the row based on the target cell value
        row = student_data.loc[student_data['UMID'] == umid]

        # Access the entire row
        selected_row = student_data.loc[row.index]
        Full_Name = selected_row.at[row.index[0], 'Full name']
        Phonetics = selected_row.at[row.index[0], 'Phonetics']

        qr_img = qr_uploader.generate_qr_code(Full_Name, umid)
        phon_image = qr_uploader.generate_phonetics(Full_Name, Phonetics, umid)

        # Create an in-memory file-like object to store the converted image data
        #image_buffer = io.BytesIO()
        
        # Save it locally for temp.
        local_path = os.path.join(os.path.dirname(__file__), f"./PDF_generation/QR_Codes/{umid}.jpg")
        local_path_phonetics = os.path.join(os.path.dirname(__file__), f"./PDF_generation/Phonetics/{umid}.jpg")
        # Save the QR code image locally
        qr_img.save(local_path, format='JPEG')
        # Save the phonetics image
        phon_image.save(local_path_phonetics, format='JPEG')

        # Read the saved image data
        with open(local_path, "rb") as image_file:
            image_data = image_file.read()
        
        audio_link = requests.get(recording_link)
        audio_content = io.BytesIO(audio_link.content)
        sound = AudioSegment.from_file(audio_content)
        # qr_img.save(image_buffer, format='JPEG')
        # image_data = image_buffer.getvalue()
        # qr_uploader.send_email(email, image_data)

    # Store it locally now.
    path_to_store = os.path.join(os.path.dirname(__file__), ".\\Anonymized_audios\\")
    audio_processor.upload_audio_locally(output_file, sound, path_to_store)
