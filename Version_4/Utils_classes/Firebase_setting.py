import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

class MessageReader:
    def __init__(self):
        try:
            # Initialize Firebase
            cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "../JSONs/firebase_credentials.json"))
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://name-pro-ad9ab-default-rtdb.firebaseio.com/'
                    })
        except ValueError as e: 
            print("The Firebase app already exists.{e}")

        self.ref_umid = db.reference('UMID')
        self.ref_linestatus = db.reference('LineStatus')
        self.ref_signal = db.reference('Signal')
        self.ref_value1 = db.reference('value')

    def get_signal(self):
        signal_snapshot = self.ref_signal.get()
        signal = signal_snapshot.get("signal1")
        return signal

    def set_umid(self, value, audio_file, scanner_no):
        self.ref_umid.set({
            'message': value,
            'audio_file': audio_file,
            'from': scanner_no
        })

    def set_value1(self, value):
        self.ref_value1.set({
            'message': value,
        })
    
    def get_value1(self):
        value_snapshot = self.ref_value1.get()
        value = value_snapshot.get("message")
        return value

    def set_linestatus_start(self, scanner_no):
        self.ref_linestatus.set({
            'message': "START",
            'from': scanner_no
        })

    def set_linestatus_end(self, scanner_no):
        self.ref_linestatus.set({
            'message': "END",
            'from': scanner_no
        })

    def get_linestatus(self):
        linestatus_snapshot = self.ref_linestatus.get()
        linestatus_msg = linestatus_snapshot.get('message')
        linestatus_from = linestatus_snapshot.get('from')
        return linestatus_msg, linestatus_from

# Usage
# reader = MessageReader()
# signal = reader.get_signal()
# reader.set_umid("value", "audio.mp3")
# reader.set_linestatus_end()
# status_msg, status_from = reader.get_linestatus()
# reader.set_linestatus_start()



