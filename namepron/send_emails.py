# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:53:37 2023

@author: benda
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd

# read the email address and password from environment variables
email_address = os.environ.get('EMAIL_ADDRESS')
email_password = os.environ.get('EMAIL_PASSWORD')

#print(type(email_address))
#print(email_password)
# set up the SMTP server
smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
smtp_server.starttls()
smtp_server.login(email_address, email_password)

# load the excel sheet containing email IDs into a pandas dataframe
excel_file = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/Students.xlsx'
df = pd.read_excel(excel_file, dtype=str)

# create a dictionary of email IDs and corresponding image file paths
#image_path = os.path.join('H:/MS 2.0/UMDearborn/Lab_Projects/face recog/face recog/QR codes')
#image_path = str(image_path)
#image_files = os.listdir(image_path)
#email_image_map = {}
umid_image_map = {}
for i, row in df.iterrows():
    image_path = os.path.join('H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/QR-code-generate')
    email = row['University mail id']
    print(email)
    umid = row['UM ID number']
    print(umid)
    #print(image_path)
    image_file = image_path + '/' + umid +'.jpg'
    #image_file = os.path.join(image_path, f'{umid}.png')
    #print(image_file)
    if os.path.isfile(image_file):
        umid_image_map[umid] = image_file

# loop through the dictionary and send an email to each recipient with their corresponding image
#for umid, image_path in umid_image_map.items():

    # create the message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = email
    msg['Subject'] = 'Test Email'
    
    # add the image as a link
    body = "Please check out your QR code image!"
    msg.attach(MIMEText(body, 'html'))
    
    # add the image as an attachment
    #image_path = os.path.join('H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/QR codes', '63402444.png')
    with open(image_file , 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename='QR_code.png')
        msg.attach(img)
    
    # send the message
    try:
        smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
smtp_server.quit()