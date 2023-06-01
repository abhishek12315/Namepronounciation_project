import PySimpleGUI as sg
import re
import json
import io
import sys
# Load the language details from the JSON file
with open('language_codes.json', 'r') as file:
    language_details = json.load(file)

# Extract the language codes and names from the language details
language_codes = list(language_details.keys())
language_names = [language_details[code] for code in language_codes]

# Define the layout of the window
layout = [
    [sg.Text('Name of the student:'), sg.Input(key='-NAME-')],
    [sg.Text('Umich email of the student:'), sg.Input(key='-EMAIL-')],
    [sg.Text('UMID of the student:'), sg.Input(key='-UMID-')],
    [sg.Text('Degree major of the student:'), sg.Input(key='-DEGREE-')],
    [sg.Text('Graduating from school:'), sg.Input(key='-SCHOOL-')],
    [sg.Text('Select the language:'), sg.Combo(language_names, default_value=language_names[0], key='-LANGUAGE-')],
    [sg.Button('Submit')]
]

# Create the window
window = sg.Window('User Input', layout)

# Define the patterns for each field
email_pattern = r'^[A-Za-z0-9._%+-]+@umich\.edu$'
umid_pattern = r'^\d{8}$'
text_pattern = r'^[A-Za-z\s]+$'

# Define error messages for each field
error_messages = {
    'Name': 'Please enter a valid name with only letters and spaces.',
    'Email': 'Please enter a valid uniquename@umich.edu email address.',
    'UMID': 'Please enter an 8-digit integer for UMID.',
    'Degree': 'Please enter a valid degree major with only letters and spaces.',
    'School': 'Please enter a valid school name with only letters and spaces.',
    'Language': 'Please select a language.'
}

# Event loop to capture user input
while True:
    event, values = window.read()

    # Check if the window is closed or the submit button is clicked
    if event == sg.WINDOW_CLOSED:
        sys.exit()
    elif event == 'Submit':
        # Retrieve the user input from the input fields
        name = values['-NAME-']
        email_id = values['-EMAIL-']
        umid = values['-UMID-']
        degree = values['-DEGREE-']
        school = values['-SCHOOL-']
        language_index = language_names.index(values['-LANGUAGE-'])
        language = language_codes[language_index]

        # Validate each field based on the corresponding pattern
        errors = []
        if not re.match(text_pattern, name):
            errors.append('Name')
        
        if not re.match(email_pattern, email_id):
            errors.append('Email')
        
        if not re.match(umid_pattern, umid):
            errors.append('UMID')
        
        if not re.match(text_pattern, degree):
            errors.append('Degree')
        
        if not re.match(text_pattern, school):
            errors.append('School')
        
        if not language:
            errors.append('Language')

        # Check if any errors occurred
        if errors:
            error_message = 'Invalid input format. Please check the following fields:\n\n'
            for field in errors:
                error_message += f'- {field}: {error_messages[field]}\n'
            sg.popup_error(error_message)
            continue

        # Proceed with the validated user input
        sg.popup("Form submitted successfully!")
        print("Name:", name)
        print("Email ID:", email_id)
        print("UMID:", umid)
        print("Degree:", degree)
        print("School:", school)
        print("Language:", language)
        break

# Close the window
window.close()


# GCP credentials
bucket_name = 'namepro1'
credentials_path = 'credentials.json'

#%%
from bigqueryloader_for_onspot import BigQueryDataLoader

loader = BigQueryDataLoader(credentials_path)
dataset_name = 'graduate_students_dataset'
table_name = 'Student_data'

loader.load_data_into_bigquery(dataset_name, table_name, name, email_id, umid, degree, school)
#%%
from on_spot_qr_code import QRCode

qr_code_folder = 'qr_code'
qr_uploader = QRCode(credentials_path)

qr_img = qr_uploader.generate_qr_code(umid)
qr_uploader.upload_qr_code_to_gcs(umid, qr_img, bucket_name, qr_code_folder)

# Create an in-memory file-like object to store the converted image data
image_buffer = io.BytesIO()
qr_img.save(image_buffer, format='JPEG')
image_data = image_buffer.getvalue()
qr_uploader.send_email(email_id, image_data)
#%%

from texttospeech import TTS

tts = TTS(credentials_path)
folder_name = 'audio_files'

output_file = tts.anonymize_umid(umid)

response = tts.synthesize_text(name, language)
tts.store_audio_in_gcs(bucket_name, folder_name, output_file, response)

