from flask import Flask, render_template
from flask_socketio import SocketIO
import sys
import time
from Utils_classes.audio_processing import Anonymized_audio
audio_processor = Anonymized_audio()
from Utils_classes.Firebase_setting import MessageReader
tracker = MessageReader()

app = Flask(__name__)
socketio = SocketIO(app)
scanner_no = 1
scanned = "Not"
def Normal_audioplay(value):
    qrdata_to_binary = audio_processor.anonymize_umid(value) # audio_file_name
    audio_file = f"{qrdata_to_binary}.mp3"
    global scanner_no
    tracker.set_umid(value, audio_file, scanner_no)


@app.route('/')
def index():
    return render_template('index2.html')

@socketio.on('update_text')
def handle_update_text(data):
    value = data.get('value', '')

    updated_text = value
        # You can send the updated text to the connected clients using socketio.emit
    socketio.emit('text_updated', updated_text)

if __name__ == '__main__':
    socketio.run(app, debug=True)
