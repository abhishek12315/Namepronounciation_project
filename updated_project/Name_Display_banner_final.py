import cv2
import numpy as np
from google.cloud import bigquery
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
#%%

try:
    # Initialize Firebase
    cred = credentials.Certificate('firebase_credentials.json')
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

# Setup camera
cap = cv2.VideoCapture(0)

# Converting cap resolution
cap.set(3, 1080)
cap.set(4, 720)

# Read logo and resize
logo = cv2.imread('Barner_2.jpg')
size_1 = 1280
size_2 = 175
logo = cv2.resize(logo, (size_1, size_2))

# Create a mask of logo
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

# Load the student data
student_data = pd.read_excel("./updated_project/Student_info.xlsx")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
   
    # Receive UMID from the QR code read. 
#    msg=requests.get("https://api.thingspeak.com/channels/2059263/fields/1")
#    msg=msg.json()['feeds'][-1]['field1']
#    print("\nThe Message sent was: \n\n"+str(msg))
    # Get a database reference
    ref = db.reference('UMID')

    # Retrieve the message from the Firebase database
    message_snapshot = ref.get()
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
    print(UMID_old)
    
    if UMID != UMID_old:
        UMID = UMID_old
        if UMID == "00000000":
            Name = ""
            College = ""
            Major = ""

        elif UMID is not None:
            # Locate the row based on the target cell value
            row = student_data.loc[student_data['UMID'] == int(UMID)]
            
            # Access the entire row
            selected_row = student_data.loc[row.index]

            Name = selected_row.at[row.index[0], 'Full name']
            College = selected_row.at[row.index[0], 'College']
            Major = selected_row.at[row.index[0], 'Major']
        else:
            Name = ""
            College = ""
            Major = ""
    
    # Region of Image (ROI), where we want to insert logo
    roi = frame[545:size_2+545, 0:size_1]  # Make a copy of the ROI
    roi[np.where(mask)] = 0
    roi += logo

    # Setting text features
    name = Name
    name_org = (160, 605)

    col = College
    col_org = (160, 640)

    major = Major
    major_org = (160, 675)

    font = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 1
    color = (255, 255, 255)
    thickness = 2

    # Name
    cv2.putText(frame, name, name_org, font, fontScale, color, thickness, cv2.LINE_AA, False)
    # College
    cv2.putText(frame, col, col_org, font, fontScale, color, thickness, cv2.LINE_AA, False)
    # Major
    cv2.putText(frame, major, major_org, font, fontScale, color, thickness, cv2.LINE_AA, False)

    # Converting normal window size to full screen
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite('Frame.png', frame)
        break

cap.release()
cv2.destroyAllWindows()
