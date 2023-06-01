# -*- coding: utf-8 -*-
"""
Created on Mon May 22 19:50:38 2023

@author: benda
"""

# importing the libraries
import cv2
import numpy as np
import csv
from google.cloud import bigquery

# UMID
UMID = ""
Name = ""
College = ""
Major = ""

def find_content_in_bigquery(project_id, dataset_id, table_id, content):
    """
    Searches for the given content in the specified BigQuery table.
    Returns True if the content is found, otherwise returns False.
    """
    client = bigquery.Client(project=project_id)
    query = f"""
        SELECT *
        FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE UM_ID_Number = @content
    """
    params = [bigquery.ScalarQueryParameter("content", "STRING", content)]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = params
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    return len(list(results)) > 0

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

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Getting the data from Google Cloud BigQuery
    project_id = "name-pro-386317"
    dataset_id = "graduate_students_dataset"
    table_id = "Student_data"
    
    if UMID:
        if find_content_in_bigquery(project_id, dataset_id, table_id, UMID):
            client = bigquery.Client(project=project_id)
            query = f"""
                SELECT *
                FROM `{project_id}.{dataset_id}.{table_id}`
                WHERE UM_ID_Number = @umid
            """
            params = [bigquery.ScalarQueryParameter("umid", "STRING", UMID)]
            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = params
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
    
    # Region of Image (ROI), where we want to insert logo
    roi = frame[545:size_2+545, 0:size_1]
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