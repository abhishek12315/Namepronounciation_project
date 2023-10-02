import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
import time

class HandScannerApp(QMainWindow):
    scanned_text_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hand Scanner App")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.scanned_label = QLabel("Scanned String:")
        self.layout.addWidget(self.scanned_label)

        self.scanned_text = QLineEdit()
        self.layout.addWidget(self.scanned_text)

        self.central_widget.setLayout(self.layout)
    
        self.scanned_text.returnPressed.connect(self.replace_scanned_text)

    def replace_scanned_text(self):
        new_text = self.scanned_text.text()
        self.scanned_label.setText(f"Scanned String: {new_text}")
        self.scanned_text.clear()
        self.scanned_text_signal.emit(new_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner_app = HandScannerApp()

    def print_new_text(new_text):
        value = new_text
        print(value)
        # while True: 
        #     "Future code here"
        #     print("something")


    # scanner_app.scanned_text_signal.connect(print_new_text)

    scanner_app.scanned_text_signal.connect(print_new_text)


    scanner_app.show()
    sys.exit(app.exec_())
