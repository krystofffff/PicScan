from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from definitions import ROOT_DIR, CSS_DIR


class AutoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" ")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Start auto mode ?")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(250, 100)
        self.layout.addWidget(self.label)

        self.h_layout = QHBoxLayout()
        self.button_accept = QPushButton("Yes")
        self.button_accept.setFixedSize(100, 50)
        self.button_accept.clicked.connect(lambda: self.selection(True))
        self.button_decline = QPushButton("No")
        self.button_decline.setFixedSize(100, 50)
        self.button_decline.clicked.connect(lambda: self.selection(False))
        self.h_layout.addStretch()
        self.h_layout.addWidget(self.button_accept)
        self.h_layout.addStretch()
        self.h_layout.addWidget(self.button_decline)
        self.h_layout.addStretch()

        self.layout.addLayout(self.h_layout)

        self.setLayout(self.layout)

        self.setFixedSize(360, 240)

        css = ["autoDialog.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def selection(self, val):
        if val:
            self.accept()
        else:
            self.close()
