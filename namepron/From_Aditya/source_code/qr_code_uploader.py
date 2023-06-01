# -*- coding: utf-8 -*-
"""
Created on Thu May 18 13:40:18 2023

@author: benda
"""

import qrcode
from PIL import ImageDraw, ImageFont
import io
import os
from google.cloud import storage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

# read the email address and password from environment variables
email_address = os.environ.get('EMAIL_ADDRESS')
email_password = os.environ.get('EMAIL_PASSWORD')

#print(type(email_address))
#print(email_password)
# set up the SMTP server
smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
smtp_server.starttls()
smtp_server.login(email_address, email_password)

#%%
class QRCodeUploader:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path

    def generate_qr_code(self, umid):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(umid)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_width, qr_height = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 18)
        label_text = "Scan Me!!"
        label_width, label_height = draw.textsize(label_text, font=font)
        label_position = ((qr_width - label_width) // 2, qr_height - label_height - 10)
        draw.text(label_position, label_text, font=font, fill="black")
        return img

    def upload_qr_code_to_gcs(self, umid, img, bucket_name, qr_code_folder):
        credentials_path = self.credentials_path
        storage_client = storage.Client.from_service_account_json(credentials_path)
        bucket = storage_client.get_bucket(bucket_name)
        image_filename = f'{umid}.jpg'
        blob = bucket.blob(f'{qr_code_folder}/{image_filename}')

        # Convert image to bytes
        image_bytes = io.BytesIO()
        img.save(image_bytes, format='JPEG')
        image_bytes.seek(0)

        # Upload image to GCS
        blob.upload_from_file(image_bytes, content_type='image/jpeg')

        print(f'QR code for UMID {umid} uploaded to GCS.')
        
    def send_email(self, email, img):
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
        with open(img , 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', filename='QR_code.jpg')
            msg.attach(img)
        
        # send the message
        try:
            smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
            print(f"Email sent to {email}")
        except Exception as e:
            print(f"Error sending email to {email}: {e}")