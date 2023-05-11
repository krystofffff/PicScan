from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame

from definitions import CSS_DIR, ASSETS_PATH, ICON_PATH
import src.managers.config_manager as cm


class PopupDialog(QDialog):
    def __init__(self, message, yes_mess=None, no_mess=None):
        super().__init__()
        self.setWindowTitle(" ")
        self.setWindowIcon(QIcon(ICON_PATH))

        if yes_mess is None:
            yes_mess = cm.tr().popup_dialog.yes
        if no_mess is None:
            no_mess = cm.tr().popup_dialog.no

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumSize(150, 50)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        if yes_mess:
            button_accept = QPushButton(yes_mess)
            button_accept.setMinimumSize(100, 50)
            button_accept.clicked.connect(lambda: self.selection(True))
            h_layout.addWidget(button_accept)
        if no_mess:
            if yes_mess:
                h_layout.addStretch()
            button_decline = QPushButton(no_mess)
            button_decline.setMinimumSize(100, 50)
            button_decline.clicked.connect(lambda: self.selection(False))
            h_layout.addWidget(button_decline)

        h_layout.addStretch()

        frame = QFrame()
        frame.setMinimumHeight(20)

        layout.addWidget(label)
        layout.addWidget(frame)
        layout.addLayout(h_layout)

        self.setLayout(layout)

        self.setMinimumSize(360, 160)

        css = ["autoDialog.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def selection(self, val):
        if val:
            self.accept()
        else:
            self.close()
