import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
import psutil


class LunaGui(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.send_button = QPushButton('Send')
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.setWindowTitle("Luna Chat")
        self.show()

        # Connect the send button
        self.send_button.clicked.connect(self.start_thread)

    def start_thread(self):
        message_thread = MessageThread(self.input_field.text())
        message_thread.message_stream.connect(self.update_chat_area)
        message_thread.start()

        self.input_field.clear()

    def update_chat_area(self, message_chunk):
        self.chat_area.append(message_chunk)


class MessageThread(QThread):
    message_stream = pyqtSignal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        # Replace the following lines with the appropriate API calls and processing
        # to handle sending and retrieving messages, as in "luna.py".

        message = self.user_input
        self.message_stream.emit(f"User: {message}")

        luna_response = f"Luna: Reply for '{message}'"  # Replace with actual Luna response
        self.message_stream.emit(luna_response)

        battery = psutil.sensors_battery()
        sys_info = f"SYSTEM INFO [BATTERY LIFE: {battery.percent}%, " \
                   f"BATTERY CHARGING: {battery.power_plugged}, " \
                   f"SYSTEM TIME: {datetime.now()}]"
        self.message_stream.emit(sys_info)


app = QApplication(sys.argv)
luna_gui = LunaGui()
sys.exit(app.exec_())
