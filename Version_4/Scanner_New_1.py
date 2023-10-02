import time
from Utils_classes.audio_processing import Anonymized_audio
audio_processor = Anonymized_audio()
from Utils_classes.Firebase_setting import MessageReader
tracker = MessageReader()

scanner_no = 1
scanned = "Not"

def Normal_audioplay(value):
    qrdata_to_binary = audio_processor.anonymize_umid(value) # audio_file_name
    audio_file = f"{qrdata_to_binary}.mp3"
    global scanner_no
    tracker.set_umid(value, audio_file, scanner_no)


while True:
    signal = tracker.get_signal()
    linestatus_msg, linestatus_from = tracker.get_linestatus()
    
    # First Check for END of line
    if linestatus_msg == "END" and linestatus_from == scanner_no:
        Text = "Line End - Please Wait" # Need to be send to HTML
        while True:
            value = input()
            if value == "Start":
                tracker.set_linestatus_start(scanner_no)
                break
            else:
                print("Line End - Please Wait")
                time.sleep(2)

    # Check for Signal and whether its scanned or not. 
    if signal == scanner_no and scanned == "Not": 
        Text = "Go ahead, scan QR code!!" # Need to be send to HTML
        value = input()
        if len(value) == 8 and value.isdigit():
            Normal_audioplay(value)
            scanned = "scanned"
        elif value == "End":
            tracker.set_linestatus_end(scanner_no)
            scanned = "Not"
        else: 
            Text = "Invalid" # Need to be send to HTML
            scanned = "Not"
        if scanned != "scanned":
            value = "00000000"
            Normal_audioplay(value)
    else:
        Text = "Please Wait" # Need to be send to HTML
        scanned = "Not"

    
