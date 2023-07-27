import cv2
import numpy as np
from google.cloud import bigquery
import requests
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
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
credentials_path = service_account.Credentials.from_service_account_file('credentials.json')

def find_content_in_bigquery(project_id, dataset_id, table_id, content):
    """
    Searches for the given content in the specified BigQuery table.
    Returns True if the content is found, otherwise returns False.
    """
    client = bigquery.Client(credentials=credentials_path, project=project_id)
    query = f"""
        SELECT *
        FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE UM_ID_Number = @content
    """
    params = [bigquery.ScalarQueryParameter("content", "STRING", content)]
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    return len(list(results)) > 0

# Setup camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open camera")
    exit()

# Read logo and resize
logo = cv2.imread('Barner_2.jpg')
# Get the size of the overlay image
overlay_height, overlay_width, _ = logo.shape

# Get the screen width and height
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a mask of logo
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

# Getting the data from Google Cloud BigQuery
project_id = "fabled-triumph-387603"
dataset_id = "graduate_students_dataset"
table_id = "Student_data"

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
        if message:
            print(f"Message retrieved from Firebase: {message}")
        else:
            print("No message found in the Firebase database.")
    else:
        print("Failed to retrieve data from Firebase.")
    
    UMID_old = str(message)   #UMID.UMID
    print(UMID_old)
    
    if UMID != UMID_old:
        UMID = UMID_old
        if find_content_in_bigquery(project_id, dataset_id, table_id, UMID):
            client = bigquery.Client(credentials=credentials_path, project=project_id)
            query = f"""
                SELECT *
                FROM `{project_id}.{dataset_id}.{table_id}`
                WHERE UM_ID_Number = @umid
            """
            params = [bigquery.ScalarQueryParameter("umid", "STRING", UMID)]
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            query_job = client.query(query, job_config=job_config)
            results = query_job.result()
        
            for row in results:
                Name = row.Full_Name
                College = row.School
                Major = row.Major
        else:
            Name = ""
            College = ""
            Major = ""
    
    # Resize the overlay image to match the width of the frame
    resized_overlay = cv2.resize(logo, (frame.shape[1], int(frame.shape[1] * overlay_height / overlay_width)))

    # Calculate the position to overlay the image (bottom-left corner)
    y_offset = frame.shape[0] - resized_overlay.shape[0]
    x_offset = 0
    
    # Overlay the image on the frame
    frame[y_offset:frame.shape[0], x_offset:x_offset + resized_overlay.shape[1]] = resized_overlay


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
