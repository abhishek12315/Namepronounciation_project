Initial version - 
1. Explained below

Version2 - Specific changes:
1. Integrated with Namecoach API
2. Instead of GCP stored everything locally
3. Used Excel sheets instead of Google form

Version3 - Specific changes:
1. Synchronization with multiple camera scanners. 
2. Audio played at the Video processing computer. 
3. Improved the structure of project. 

Folder structure - 
Version*/
|-- improved_QRcode_read.py (QR code scan and Audio play)
|-- Name_Display_banner_final.py (Printing students Information on live feed)
|-- Pre_processing.py 
|--/ Anonymized_audios/
|   |-- All audio_files
|
|-- / Audio_monitoring
|	|-- play_audio.py  - Play all audio from Anonymized_audios/ 
|	|-- audio_names.txt - Information of played audios
|
|-- JSONs/
|   |-- firebase_credentials.json - Store your credential here. 
|	|-- No_Audio_file.json 	- List of email ids with no audio on namecoach
|	|-- sent_emails.json	- List of email ids to which QR code send. (Remove from here to sent the QR code again)
|	|-- Student_info.xlsx
|
|-- Temp_Namecoach_audio/ - For experiment purpose (Remove from main version)
|
|-- Utils_classes/
|   |-- audio_processing.py		- Anonymization and Normalization
|   |-- namecoach.py			- Access namecoach get binary form audio file
|   |-- email_qrcode.py			- email qr code
|
|-- Video_banner/
|   |-- Banner.JPG
|   |-- Frame.PNG
|   |-- logo.JPG

Project Objective - 
1.	The graduation ceremony is an important event that marks the culmination of years of hard work and academic achievements for students. It is a time of celebration and recognition, where students eagerly wait to have their names called out and walk across the stage to receive their diplomas. However, amidst the excitement and anticipation, mispronunciations of names can sometimes occur, leading to moments of embarrassment and frustration.
 
2.	Mispronunciations at graduation ceremonies can happen for various reasons. Firstly, the sheer number of graduates can pose a challenge for the individuals announcing the names. With hundreds or even thousands of students graduating, it becomes a daunting task to accurately pronounce every single name correctly. This can be especially challenging for names that are unique or have unconventional spellings, as they may not be familiar to the announcer. Another factor contributing to mispronunciations is the diversity of student populations. Graduation ceremonies often include students from different cultural backgrounds, each with their own distinct names and pronunciations. While efforts are made to gather correct pronunciation information, it is not always possible to obtain accurate details for every student. As a result, mistakes can occur despite the best intentions of the organizers. Mispronunciations can have a significant impact on students' experiences during the graduation ceremony. For many, this event represents the pinnacle of their academic journey, and having their names mispronounced can feel disheartening and diminish the sense of personal accomplishment. 

3.	To elevate the students' graduation ceremony experience, we have an innovative proposal for enhancing the ceremony through the implementation of a personalized audio system. This system will allow students to create unique audio files, adding a truly individualized touch to their special moments. Moreover, our software will seamlessly integrate with the live feed camera, providing an enriched visual aspect to the ceremony. By combining both visual and informational elements, we aim to create a truly remarkable experience for all attendees. In addition to capturing the moment when each student receives their degree, the camera feed will showcase essential student information, including their name, school details, and major. This comprehensive integration ensures that every attendee can fully recognize and celebrate each student's achievements. By merging the excitement of the moment with the necessary details, we will craft a captivating and engaging experience for all, making the graduation ceremony a truly memorable event for everyone involved.

Initial Version explained: 
Description of proposed solution using Flowchart:
1.	Working of Project: In the flowchart provided, both systems initiate their operation simultaneously. The first system scans the QR code to retrieve the student ID and plays the corresponding audio file. Additionally, it shares the student ID with the second system through the Firebase API. The second system then retrieves the student's information from Google Cloud and displays it on the live feed. In the meantime, if no QR code is scanned it continues to display the last scanned QR code-related student data. 
![Alt text](image.png)

2.	Preprocessing: The diagram provided below illustrates the preprocessing flow. In this process, we retrieve the student's information and audio file by utilizing either the namecoach API or Google form. To ensure anonymity, the audio file is made anonymous, and we also normalize the audio file to maintain consistent loudness across all files. Additionally, we convert other supporting audio files, such as m4A and WAV, to the mp3 format for consistency. Subsequently, the audio file is transferred to Google Storage. If an audio file with the same name already exists in the storage after anonymization, it is replaced with the latest audio file. 

The student's name, major, and school-related text information are stored in a BigQuery database in tabular format. Similarly, if data related to the same student Id (Unique Identifier) is available, it is replaced with the most recent data.

Once a QR code is generated, it is stored in cloud storage, and an email is sent to the corresponding students at their respective email addresses.
 ![Alt text](image-1.png)
 
3.	On spot form: The On-spot form, GUI window for form is rendered which collects the necessary student data. This data is initially stored in variables, and Google's text-to-speech API is utilized to generate an AI voice based on the dialect and language. After anonymization and normalization, the audio file is saved in mp3 format and stored in Google Storage.

The data collected through the form is stored in the same BigQuery database used for preprocessing. If any existing data matches the student ID, it is replaced with the data received from this form.

A QR code is created, uploaded to Google Storage, and then sent to the student's email address.
![Alt text](image-2.png)