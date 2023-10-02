import sys
import time
from Utils_classes.audio_processing import Anonymized_audio
audio_processor = Anonymized_audio()
from Utils_classes.Firebase_setting import MessageReader
tracker = MessageReader()
from PyQt5.QtWidgets import QApplication
from Utils_classes.GUI_setting import CenteredTextDisplay


app = QApplication([])
window = CenteredTextDisplay()
def update_gui_text(text):
    window.display_text(text)
    QApplication.processEvents()

scanner_no = 1
scanned = "Not"
def Normal_audioplay(value):
    qrdata_to_binary = audio_processor.anonymize_umid(value) # audio_file_name
    audio_file = f"{qrdata_to_binary}.mp3"
    global scanner_no
    tracker.set_umid(value, audio_file, scanner_no)

# def print_new_text(new_text):
#         value = new_text
#         tracker.set_value1(value)
#         print(value)

# window.scanned_text_signal.connect(print_new_text)

old_value = "00000"
while True:
    signal = tracker.get_signal()
    linestatus_msg, linestatus_from = tracker.get_linestatus()
    
    # First Check for END of line
    if linestatus_msg == "END" and linestatus_from == scanner_no:
        Text = "Line End - Please Wait"
        update_gui_text(Text)
        while True:
            # value = tracker.get_value1()
            value = input()
            if value != old_value: 
                old_value = value
                if value == "Start":
                    tracker.set_linestatus_start(scanner_no)
                    break
                elif value == "Quit":
                    app.quit()  # Quit the application
                    value = "00000"
                    tracker.set_value1(value)
                    sys.exit()
                else:
                    time.sleep(3)
            else:
                pass

    # Check for Signal and whether its scanned or not. 
    if signal == scanner_no and scanned == "Not": 
        Text = "Go ahead, scan QR code!!"
        update_gui_text(Text)
        # value = tracker.get_value1()
        value = input()
        if value != old_value:
            old_value = value
            if len(value) == 8 and value.isdigit():
                Normal_audioplay(value)
                scanned = "scanned"
            
            elif value == "End":
                tracker.set_linestatus_end(scanner_no)
                scanned = "Not"

            elif value == "Quit":
                app.quit()  # Quit the application
                value = "00000"
                tracker.set_value1(value)
                sys.exit()
            
            else: 
                Text = "Invalid"
                update_gui_text(Text)
                time.sleep(3)
                scanned = "Not"
            
            if scanned != "scanned":
                value = "00000000"
                Normal_audioplay(value)
            time.sleep(3)
        else:
            time.sleep(3)
    else:
        Text = "Please Wait" 
        update_gui_text(Text)
        scanned = "Not"

    
