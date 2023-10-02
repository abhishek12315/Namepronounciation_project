import sys
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


def calling_func(value, old_value): 
    signal = tracker.get_signal()
    linestatus_msg, linestatus_from = tracker.get_linestatus()
    
    # First Check for END of line
    if linestatus_msg == "END" and linestatus_from == scanner_no:
        if value != old_value: 
            old_value = value
            if value == "Start":
                tracker.set_linestatus_start(scanner_no)
                return "Line Started!! Scan Next"
            else:
                time.sleep(3)
        else:
            pass
        return "Line End - Please Wait"

    # Check for Signal and whether its scanned or not. 
    if signal == scanner_no and scanned == "Not": 
        if value != old_value:
            old_value = value
            if len(value) == 8 and value.isdigit():
                Normal_audioplay(value)
                scanned = "scanned"
                return "Done"
            
            elif value == "End":
                tracker.set_linestatus_end(scanner_no)
                scanned = "Not"
            
            else: 
                time.sleep(3)
                scanned = "Not"
                return "Invalid"
            
            if scanned != "scanned":
                value = "00000000"
                Normal_audioplay(value)
            time.sleep(3)
        else:
            time.sleep(3)
        return "Go ahead, scan QR code!!"
    else:
        scanned = "Not"
        return "Please Wait" 

    
