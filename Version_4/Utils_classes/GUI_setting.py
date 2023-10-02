import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,QLineEdit 
from PyQt5.QtCore import Qt, pyqtSignal, QThread

class CenteredTextDisplay(QMainWindow):
    scanned_text_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Centered Text Display")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        # self.scanned_text = QLineEdit()
        # self.layout.addWidget(self.scanned_text)

        # self.central_widget.setLayout(self.layout)

        # self.scanned_text.returnPressed.connect(self.replace_scanned_text)
        
    # def replace_scanned_text(self):
    #     new_text = self.scanned_text.text()
    #     self.scanned_text.clear()
    #     self.scanned_text_signal.emit(new_text)

    def display_text(self, text):
        self.label.setText(text)
        self.label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333; background-color: #f0f0f0;"
            "border: 2px solid #666; padding: 20px; border-radius: 10px;"
        )
        self.show()

def main():
    app = QApplication(sys.argv)
    window = CenteredTextDisplay()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
