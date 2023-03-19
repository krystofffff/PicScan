from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame

from definitions import CSS_DIR


class PopupDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle(" ")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumSize(150, 50)

        h_layout = QHBoxLayout()
        button_accept = QPushButton("Yes")
        button_accept.setFixedSize(100, 50)
        button_accept.clicked.connect(lambda: self.selection(True))
        button_decline = QPushButton("No")
        button_decline.setFixedSize(100, 50)
        button_decline.clicked.connect(lambda: self.selection(False))
        h_layout.addStretch()
        h_layout.addWidget(button_accept)
        h_layout.addStretch()
        h_layout.addWidget(button_decline)
        h_layout.addStretch()

        frame = QFrame()
        frame.setMinimumHeight(20)

        layout.addWidget(label)
        layout.addWidget(frame)
        layout.addLayout(h_layout)

        self.setLayout(layout)

        self.setFixedSize(360, 160)

        css = ["autoDialog.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def selection(self, val):
        if val:
            self.accept()
        else:
            self.close()
