import sys
import cv2
import pygame
from pyzbar.pyzbar import decode
import numpy as np
import os
os.getcwd()

os.chdir('C:/Users/palla/Desktop/namepron/Audio_files')
flag = False

def qrDataToBinary(dec_val):
    def decimalToBinary(n):
        return bin(n).replace("0b", "")

    val2 = "1101"
    str1 = str(decimalToBinary(dec_val))
    val1 = str1
    
    if len(sys.argv) > 1:
        val1 = str(sys.argv[1])

    if len(sys.argv) > 2:
        val2 = str(sys.argv[2])
    
    def showpoly(a):
        str1 = ""
        nobits = len(a)

        for x in range(0, nobits-2):
            if (a[x] == '1'):
                if (len(str1) == 0):
                    str1 += "x**"+str(nobits-x-1)
                else:
                    str1 += "+x**"+str(nobits-x-1)

        if (a[nobits-2] == '1'):
            if (len(str1) == 0):
                str1 += "x"
            else:
                str1 += "+x"

        if (a[nobits-1] == '1'):
            str1 += "+1"

    def to_list(x):
        return [int(bit) for bit in x]

    def to_string(x):
        return ''.join(str(bit) for bit in x)

    def divide(val1, val2):
        a = to_list(val1)
        b = to_list(val2)
        working = to_string(val1) + "\n"

        res = ""
        addspace = ""

        while len(b) <= len(a) and a:
            if a[0] == 1:
                del a[0]
                for j in range(len(b) - 1):
                    a[j] ^= b[j + 1]
                if len(a) > 0:
                    working += addspace + to_string(b) + "\n"
                    working += addspace + "-" * len(b) + "\n"
                    addspace += " "
                    working += addspace + to_string(a) + "\n"
                    res += "1"
            else:
                del a[0]
                working += addspace + "0" * len(b) + "\n"
                working += addspace + "-" * len(b) + "\n"
                addspace += " "
                working += addspace + to_string(a) + "\n"
                res += "0"

        return to_string(a)


    showpoly(val1)
    showpoly(val2)

    strzeros = "0" * (len(val2) - 1)
    val3 = val1 + strzeros
    res = divide(val3, val2)
    return val1 + res

def decoder(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    for barcode in barcodes:
        # Extract barcode information
        points = barcode.polygon
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        
        # Draw polygon around the barcode
        pts = cv2.convexHull(np.array(points, np.int32))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        
        # Display barcode information on the image
        cv2.putText(image, f"Data: {barcodeData} | Type: {barcodeType}", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
        # Convert barcode data to binary
        binary_data = qrDataToBinary(int(barcodeData))
        
        # Play the corresponding audio file based on the binary data
        audio_file = f"{binary_data}.mp3"
        print(audio_file)
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): # This means music is being played. 
                global flag
                flag = True
                continue
            print(f"Playing {audio_file}")
        except FileNotFoundError as e:
            print(f"FileNotFoundError successfully handled:\n{e}")
        except pygame.error:
            print("Error: Audio file is not playable.")
    
    return 0

def read_qr_code():
    cap = cv2.VideoCapture(1)
    start_time = cv2.getTickCount()
    qr_code_scanned = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_time = cv2.getTickCount()
        elapsed_time = (current_time - start_time) / cv2.getTickFrequency()
        
        if elapsed_time >= 10.0:
            cv2.putText(frame, f"Scan Now", (225, 225),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            if qr_code_scanned:
                qr_code_scanned = False
                global flag
                flag = False
                start_time = cv2.getTickCount()
            else:
                if (decoder(frame) == 0) & (flag == True): # That means audio is played and QR code scanned.  
                    qr_code_scanned = True
                cv2.imshow('Image', frame)
        else:
            cv2.putText(frame, f"Please wait: {10 - elapsed_time:.1f}s", (75, 225),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            cv2.imshow('Image', frame)
        print(elapsed_time)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

read_qr_code()
