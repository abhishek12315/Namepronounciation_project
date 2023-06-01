from google.oauth2 import service_account
from google.auth.transport.requests import Request
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
import requests
import struct
import gdown
from pydub import AudioSegment
import sys
#%%
# read the email address and password from environment variables
email_address = os.environ.get('EMAIL_ADDRESS')
email_password = os.environ.get('EMAIL_PASSWORD')

smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
smtp_server.starttls()
smtp_server.login(email_address, email_password)

#Create a QR code instance
qr = qrcode.QRCode(version=1, box_size=10, border=4)

def authenticate():
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    return credentials

from googleapiclient.discovery import build


def get_form_responses(form_id):
    service = build('forms', 'v1', credentials=authenticate())
    response = service.forms().responses().list(formId='1FvJGgdUXZc6lwd3GeZ42Dy8BmLZkyQQIBrgQK2hmF5k').execute()
    #response = service.forms().responses().get(formId="1FvJGgdUXZc6lwd3GeZ42Dy8BmLZkyQQIBrgQK2hmF5k", fullResource=True).execute()

    return response

responses = get_form_responses('1FvJGgdUXZc6lwd3GeZ42Dy8BmLZkyQQIBrgQK2hmF5k')
print(responses)


#%%    
# Specify the directory to save the downloaded files
download_dir = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/Input_audio_files/UMID_audio'
temp_dir = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/Input_audio_files/temp'

for response in responses['responses']:
    #if '19eca6e5' in response['answers']:
        #QR Code generation using UMID
        umid_details = response['answers']['0e0e5a68']['textAnswers']['answers'][0]
        umid = umid_details['value']
        print(umid)
        qr.clear()
        qr.add_data(umid)
        qr.make(fit=True)
        img: PilImage = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_width, qr_height = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 18)
        label_text = "Scan Me!!"
        label_width, label_height = draw.textsize(label_text, font=font)
        label_position = ((qr_width - label_width) // 2, qr_height - label_height - 10)
        draw.text(label_position, label_text, font=font, fill="black")
        #plt.imshow(img)
        #save image to a folder
        image_path = os.path.join('H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/QR-code-generate', f'{umid}.jpg')
        img.save(image_path, format='JPEG')
        
        #Downloading and converting audio files to .mp3
        file_details = response['answers']['19eca6e5']['fileUploadAnswers']['answers'][0]
        print(file_details)
        file_id = file_details['fileId']
        file_name = file_details['fileName']
        url = f"https://drive.google.com/uc?id={file_id}"
        output_file = f'{umid}'  # Set the output file name
        output_path = os.path.join(temp_dir, output_file)
        final_output_path = os.path.join(download_dir, output_file)# Set the output file path
        gdown.download(url, output_path, quiet=False)
        #response = requests.get(url)

        # Load the downloaded audio file
        sound = AudioSegment.from_file(output_path)
        # Convert the audio file to mp3 format
        if not final_output_path.endswith('.mp3'):
            final_output_path = os.path.splitext(final_output_path)[0] + '.mp3'
            sound.export(final_output_path, format='mp3')

        print(f"Downloaded audio file: {umid}.mp3")
        
#%%

for filename in os.listdir(download_dir):
    if os.path.isfile(os.path.join(download_dir, filename)):
        name, extension = os.path.splitext(filename)
        print(name)
        dec_val = int((name))
        
    def decimalToBinary(n):
        return bin(n).replace("0b", "")
        
    
    val2="1101"
    str1 = ""
    
    str1 = decimalToBinary(dec_val)
    val1= str1
    print(str1)
    
    if (len(sys.argv)>1):
            val1=str(sys.argv[1])
    
    if (len(sys.argv)>2):
            val2=str(sys.argv[2])
    
    
    def showpoly(a):
    	str1 = ""
    	nobits = len(a)
    
    
    	for x in range (0,nobits-2):
    		if (a[x] == '1'):
    			if (len(str1)==0):
    				str1 +="x**"+str(nobits-x-1)	
    			else: 
    				str1 +="+x**"+str(nobits-x-1)
    
    	if (a[nobits-2] == '1'):
    		if (len(str1)==0):
    			str1 +="x"
    		else:
    			str1 +="+x"
    
    	if (a[nobits-1] == '1'):
    		str1 +="+1"
    
    	print (str1)
    	
    
    def toList(x):
    	l = []
    	for i in range (0,len(x)):
    		l.append(int(x[i]))
    	return (l)
    def toString(x):
    	str1 =""
    	for i in range (0,len(x)):
    		str1+=str(x[i])
    	return (str1)
    
    def divide(val1,val2):
    	a = toList(val1)
    	b = toList(val2)
    	working=toString(val1)+"\n"
    
    	res=""
    	addspace=""
    
    	while len(b) <= len(a) and a:
                if a[0] == 1:
                		del a[0]
                		for j in range(len(b)-1):
                    			a[j] ^= b[j+1]
                		if (len(a)>0):
                				working +=addspace+toString(b)+"\n"
                				working +=addspace+"-" * (len(b))+"\n"
                				addspace+=" "
                				working +=addspace+toString(a)+"\n"
                				res+= "1"
                else:
                    del a[0]
                    working +=addspace+"0" * (len(b))+"\n"
                    working +=addspace+"-" * (len(b))+"\n"
                    addspace+=" "
                    working +=addspace+toString(a)+"\n"
                    res+="0"
    
    
    	print ("Result is\t",res)
    	print ("Remainder is\t",toString(a))
    
    	print ("Working is\t\n\n",res.rjust(len(val1)),"\n",)
    	print ("-" * (len(val1)),"\n",working)
    
    	return toString(a)
    
    print ("Binary form:\t",val1," divided by ",val2)
    print ("")
    showpoly(val1)
    showpoly(val2)
    
    strzeros=""
    strzeros = strzeros.zfill(len(val2)-1)
    val3=val1+strzeros
    
    print ("")
    print ("Binary form (added zeros):\t",val3," divided by ",val2)
    
    res=divide(val3,val2)
    final_val = val1+res
    print ("Transmitted value is:\t",final_val)
    
    new_folder_path = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/audio_files/'
    #new_prefix = final_val
    
    

    new_file_path = os.path.join(new_folder_path, final_val + extension)
    os.rename(os.path.join(download_dir, filename), new_file_path)
    