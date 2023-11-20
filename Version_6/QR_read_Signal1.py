import sys
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

try:
    # Initialize Firebase
    cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "./JSONs/firebase_credentials.json"))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://name-pro-ad9ab-default-rtdb.firebaseio.com/'
            })
except ValueError as e: 
    print("The Firebase app already exists.{e}")


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
    scanned = "Not Scanned"

    for barcode in barcodes:
        # Extract barcode information
        points = barcode.polygon
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        
        # Draw polygon around the barcode
        pts = cv2.convexHull(np.array(points, np.int32))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        
        # Display barcode information on the imageqqq
        cv2.putText(image, f"Data: {barcodeData} | Type: {barcodeType}", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
        #Updating UMID, Send the UMID to cloud. 
        msg=str(barcodeData)
        print(msg)
        # Check if the variable is an integer and has 8 digits
        if len(str(barcodeData)) == 8:
           # Convert barcode data to binary 
            binary_data = qrDataToBinary(int(barcodeData))
            scanned = "scanned"
        else:
            binary_data = 00000000
            cv2.putText(image, f"Invalid QR code", (75, 125),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        
        # Play the corresponding audio file based on the binary data
        audio_file = f"{binary_data}.mp3"
        
        # Get a database reference
        ref = db.reference('UMID')
        # Push the message to the Firebase database
        ref.set({
            'message': msg,
            'audio_file': audio_file,
            'from': 1
            })
        print("\nYour message has successfully been sent!")

    return scanned


def read_qr_code():
    cap = cv2.VideoCapture(0)
    start_time = cv2.getTickCount()
    qr_code_scanned = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Get a database reference
        ref1 = db.reference('Signal')
        current_time = cv2.getTickCount()
        elapsed_time = (current_time - start_time) / cv2.getTickFrequency()

        # Retrieve the message from the Firebase database
        signal_snapshot = ref1.get()
        if signal_snapshot:
            signal = signal_snapshot.get("signal1")
            if signal == 1:
                if elapsed_time >= 10.0:
                    cv2.putText(frame, f"Scan Now", (225, 225),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    
                    if qr_code_scanned:
                        qr_code_scanned = False
                        start_time = cv2.getTickCount()
                    else:
                        if ((decoder(frame) == "scanned")):
                            qr_code_scanned = True
                            print("decoder")
                        cv2.imshow('Image', frame)
                else:
                    cv2.putText(frame, f"Please wait: {10 - elapsed_time:.1f}s", (75, 225),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    cv2.imshow('Image', frame)
            else:
                qr_code_scanned = False
                text = f"Please wait." # Scanner is busy on the other end.
                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)

                # Calculate the position to center the text on the frame
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = (frame.shape[0] + text_size[1]) // 2

                cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                #cv2.putText(frame, f"Please wait. Scanner is busy on the other end.", (75, 225),
                        #cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                cv2.imshow('Image', frame)

        # print(elapsed_time)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    ## Get a database reference
    # ref = db.reference('UMID')
    # ref.set({
    #         'message': "0",
    #         'audio_file': "0",
    #         'from': 1
    #         })

read_qr_code()