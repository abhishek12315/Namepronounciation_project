# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:34:53 2023

@author: benda
"""

import os
import pandas as pd
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from matplotlib import pyplot as plt
import numpy as np

# load the excel sheet containing email IDs into a pandas dataframe
excel_file = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/Students.xlsx'
df = pd.read_excel(excel_file, dtype=str)
# create a QR code instance
qr = qrcode.QRCode(version=1, box_size=10, border=4)

# read the email address and password from environment variables
#email_address = os.environ.get('EMAIL_ADDRESS')
#email_password = os.environ.get('EMAIL_PASSWORD')

#print(type(email_address))
#print(email_password)
# set up the SMTP server
#smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
#smtp_server.starttls()
#smtp_server.login(email_address, email_password)


#email = []
#umid = []
for i, row in df.iterrows():
    
    umid = row['UM ID number']
    #email = row['Email-id']
    
    print(umid)

# set data to be encoded
    #for id in umid:
    qr.clear()
            # add data to the QR code instance
    qr.add_data(umid)
        
            # make the QR code
    qr.make(fit=True)
        
            # create an image from the QR code instance
    img: PilImage = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            #print(type(id))
            # add a logo to the center of the QR code
            #logo = Image.open("logo.jpg")
            #logo_width, logo_height = logo.size
    qr_width, qr_height = img.size
            #logo_position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)
            #img.paste(logo, logo_position)
        
            # add a text label to the bottom of the QR code
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 18)
    label_text = "Scan Me!!"
    label_width, label_height = draw.textsize(label_text, font=font)
    label_position = ((qr_width - label_width) // 2, qr_height - label_height - 10)
    draw.text(label_position, label_text, font=font, fill="black")
            #plt.imshow(img)
            #plt.show()
            
    
            # save the image
    image_path = os.path.join('H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/QR-code-generate', f'{umid}.jpg')
    img.save(image_path, format='JPEG')
            
            # create the message
            #msg = MIMEMultipart()
            #msg['From'] = email_address
            #msg['To'] = email
            #msg['Subject'] = 'Test Email'
            # add the image as a link
          #  body = "Please check out your QR code image!"
           # msg.attach(MIMEText(body, 'html'))
            
            #img = np.asarray(img)
           # img = MIMEImage(img)
            #img.add_header('Content-Disposition', 'attachment', filename='QR_code.png')
            #msg.attach(img)
            #smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())  
#smtp_server.quit()
        
        
        