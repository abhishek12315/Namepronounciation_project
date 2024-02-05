import cv2
import numpy as np
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import threading
import pygame
import io
import time

try:
    # Initialize Firebase
    cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "./JSONs/firebase_credentials.json"))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://name-pro-ad9ab-default-rtdb.firebaseio.com/'
            })
except ValueError as e: 
    print("The Firebase app already exists.")

# UMID
UMID = ""
UMID_old = ""
Name = ""
College = ""
Major = ""

# Create a green frame
green_frame = np.zeros((1920, 2560, 3), np.uint8)
green_frame[:, :] = (68, 255, 59)  # Set color to green

# Read logo and resize
logo = cv2.imread(os.path.join(os.path.dirname(__file__),'./Video_banner/Banner_2560.jpg'))
size_1 = 2560
size_2 = 466
logo = cv2.resize(logo, (size_1, size_2))

# Create a mask of logo
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

# Load the student data
student_data = pd.read_excel(os.path.join(os.path.dirname(__file__), "./JSONs/Student_info.xlsx"))

def play_audio(audio_file_path, from_sys):
    try:
        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        audio_stream = io.BytesIO(audio_data)
        ref1 = db.reference("Signal")
        if (from_sys == 1):
                ref1.set({
                    "signal1": 2
                })
        elif (from_sys == 2):
            ref1.set({
                "signal1": 1
            })
        time.sleep(0.5)  # Delay of 1 sec for playing audio
        pygame.mixer.init()
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play() # playing time consumed. 
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
            continue            
        print(f"Playing {audio_file}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError successfully handled:\n{e}")
    except pygame.error:
        print("Error: Audio file is not playable.")

while True:
    # Capture frame-by-frame
    frame = green_frame.copy()

    # Get a database reference
    ref = db.reference('UMID')
    Linestatus = db.reference('LineStatus')
    ref1 = db.reference("Signal")

    # Retrieve the message from the Firebase database
    message_snapshot = ref.get()
    Linestatus_snapshot = Linestatus.get()
    Linestatus_msg = Linestatus_snapshot.get('message')
    Linestatus_From = Linestatus_snapshot.get('from')

    if message_snapshot:
        message = message_snapshot.get('message')
        if len(str(message)) == 8:
            print(f"Message retrieved from Firebase: {message}")
        else:
            message = "00000000"
            print("No message found in the Firebase database.")
    else:
        print("Failed to retrieve data from Firebase.")
    
    UMID_old = str(message)   #UMID.UMID
    
    if Linestatus_msg == "START":
        Linestatus.set({
            'message': 0,
            'from': 0
            })
        if Linestatus_From == 1:
            ref1.set({
            "signal1": 2
            })
        else:
            ref1.set({
            "signal1": 1
            })
    elif Linestatus_msg == "END":
        if Linestatus_From == 1:
            ref1.set({
            "signal1": 2
            })
        else:
            ref1.set({
            "signal1": 1
            })

    if UMID != UMID_old:
        UMID = UMID_old
        if UMID == "00000000":
            Name = ""
            College = ""
            Major = ""

        elif UMID is not None:

            audio_file = message_snapshot.get('audio_file')
            from_sys = message_snapshot.get('from')

            # print(audio_file)
            audio_file_path = os.path.join(os.path.dirname(__file__), f"./Anonymized_audios/{audio_file}")
        
            # audio_file_path = f"./updated_project/Anonymized_audios/11110001110111000111001100111.mp3"
            audio_thread = threading.Thread(target=play_audio, args=(audio_file_path, from_sys))
            audio_thread.start()
            
            # Locate the row based on the target cell value
            row = student_data.loc[student_data['UMID'] == int(UMID)]

            # Access the entire row
            selected_row = student_data.loc[row.index]
            Name = selected_row.at[row.index[0], 'Diploma Name']
            # College = selected_row.at[row.index[0], 'College']
            # Major = selected_row.at[row.index[0], 'Major']

        else:
            Name = ""
            College = ""
            Major = ""
    
    # Region of Image (ROI), where we want to insert logo
    roi = frame[1920-size_2:1920, 0:size_1]  # Make a copy of the ROI
    roi[np.where(mask)] = 0
    roi += logo

    # Setting text features
    name = Name
    name_org = (340, 1750)

    # col = College
    # col_org = (160, 640)

    # major = Major
    # major_org = (160, 675)

    # Define fonts
    nunito_sans_font_path = os.path.join(os.path.dirname(__file__), f"./Nunito_Sans/NunitoSans-Italic-VariableFont_YTLC,opsz,wdth,wght.ttf")  
    arial_font = cv2.FONT_HERSHEY_DUPLEX

    # Try to load Nunito Sans font
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.FONT_HERSHEY_TRIPLEX
        fontScale = 5
        color = (255, 255, 255)
        thickness = 8

        # Name
        cv2.putText(frame, name, name_org, font, fontScale, color, thickness, cv2.LINE_AA, False)

    except cv2.error:  # Font loading failed, fallback to Arial
        font = arial_font
        fontScale = 5
        color = (255, 255, 255)
        thickness = 8

        # Name
        cv2.putText(frame, name, name_org, font, fontScale, color, thickness, cv2.LINE_AA, False)

    # College
    # cv2.putText(frame, col, col_org, font, fontScale, color, thickness, cv2.LINE_AA, False)
    # # Major
    # cv2.putText(frame, major, major_org, font, fontScale, color, thickness, cv2.LINE_AA, False)

    # Converting normal window size to full screen
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite(os.path.join(os.path.dirname(__file__),'./Video_banner/Frame.png'), frame)
        break

cv2.destroyAllWindows()

ref = db.reference('UMID')
# Push the message to the Firebase database
ref.set({
    'message': 0,
    'audio_file': 0,
    'from': 0
    })
ref1 = db.reference("Signal")
ref1.set({
    "signal1": 1
    })

