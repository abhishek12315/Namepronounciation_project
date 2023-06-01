import io

credentials_path = 'credentials.json'
bucket_name = 'namepro1'


#%%

from google_form_extractor import GoogleFormExtractor

# Create an instance of the GoogleFormExtractor class
extractor = GoogleFormExtractor('credentials.json')

# Use the methods of the class
form_id = '1FvJGgdUXZc6lwd3GeZ42Dy8BmLZkyQQIBrgQK2hmF5k'
responses = extractor.get_form_responses(form_id)
folder_name = 'Students_data'
file_name = 'students_data.txt'
extractor.store_responses_in_gcs(bucket_name,folder_name, file_name, responses)


#%%
from bigquery_loader import BigQueryLoader

# Create an instance of the BigQueryLoader class
loader = BigQueryLoader(credentials_path)

# Use the methods of the class
dataset_name = 'graduate_students_dataset'
table_name = 'Student_data'
loader.create_bigquery_table(dataset_name, table_name)

transformed_responses = loader.transform_responses(responses)

loader.load_data_into_bigquery(dataset_name, table_name, transformed_responses)

print('Responses stored in Google Cloud Storage and BigQuery.')

#%%

from qr_code_uploader import QRCodeUploader


qr_code_folder = 'qr_code'
# Create an instance of the QRCodeUploader class
qr_uploader = QRCodeUploader(credentials_path)


for response in responses['responses']:
    email = response['answers']['69a71cb8']['textAnswers']['answers'][0]['value']
    umid = response['answers']['0e0e5a68']['textAnswers']['answers'][0]['value']
    qr_img = qr_uploader.generate_qr_code(umid)
    qr_uploader.upload_qr_code_to_gcs(umid, qr_img, bucket_name, qr_code_folder)

    # Create an in-memory file-like object to store the converted image data
    image_buffer = io.BytesIO()
    qr_img.save(image_buffer, format='JPEG')
    image_data = image_buffer.getvalue()
    
    qr_uploader.send_email(email, image_data)
    
#%%

from audio_processing import Anonymized_audio

#Create an instance of Anonymized_audio class
audio_processor = Anonymized_audio(credentials_path)
audio_folder = 'audio_files'

for response in responses['responses']:
    umid = response['answers']['0e0e5a68']['textAnswers']['answers'][0]['value']
    output_file = audio_processor.anonymize_umid(umid)
    audio_processor.upload_audio_to_gcs(response, bucket_name, audio_folder, output_file)
