# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 20:55:35 2022

@author: sakareem
"""

import os
#from playsound import playsound
from google.cloud import storage
import pygame
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import struct
import sys
import io


# Initialize Google Cloud Storage client
credentials_path = 'credentials.json'
storage_client = storage.Client.from_service_account_json('credentials.json')

# Specify the GCS bucket and folder path for audio files
bucket_name = "graduate_students_data"
folder_path = "student_audio_files/"

# Create a bucket object
bucket = storage_client.get_bucket(bucket_name)




####################################
#dec_val = int(input()) 

def qrDataToBinary(dec_val):
    #print("Dec_val :" + str(dec_val))
    def decimalToBinary(n):
        return bin(n).replace("0b", "")
        
    
    val2="1101"
    str1 = ""
    
    str1 = str(decimalToBinary(dec_val))
    val1= str1
    #print(str1)
    
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
    
    	#print (str1)
    	
    
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
    
    
    	#print ("Result is\t",res)
    	#print ("Remainder is\t",toString(a))
    
    	#print ("Working is\t\n\n",res.rjust(len(val1)),"\n",)
    	#print ("-" * (len(val1)),"\n",working)
    
    	return toString(a)
    
    #print ("Binary form:\t",val1," divided by ",val2)
    #print ("")
    showpoly(val1)
    showpoly(val2)
    
    strzeros=""
    strzeros = strzeros.zfill(len(val2)-1)
    val3=val1+strzeros
    
    #print ("")
    #print ("Binary form (added zeros):\t",val3," divided by ",val2)
    
    res=divide(val3,val2)
    #print ("Transmitted value is:\t",val1+res)
    return val1+res

####################################


def decoder(image, bucket):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data: " + str(barcodeData) + " | Type " + str(barcodeType)
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        #print("Barcode: "+barcodeData +" | Type: "+barcodeType)
        str2 = qrDataToBinary(int(barcodeData))
        #print("str2: " + str2)
        
        s = str2 + '.mp3'
        
        blob = bucket.blob(folder_path + s)
        audio_data = blob.download_as_bytes()
        audio_stream = io.BytesIO(audio_data)
        
        try:
            
            pygame.mixer.init()
            pygame.mixer.music.load(audio_stream)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                continue
        #playsound(s)
            print("Playing " + s )
        except FileNotFoundError as e:
            print(f"FileNotFoundError successfully handled\n"
                      f"{e}")
        except pygame.error:
            # If an error occurs, print a message to the console
            print("Error: Audio file is not playable.")
        
            
        return 0
                
    
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if decoder(frame, bucket) ==1:
        break
    cv2.imshow('Image', frame)
    
    code = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

