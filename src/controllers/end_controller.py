import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame

from definitions import CSS_DIR
import src.managers.config_manager as cm
import src.managers.data_manager as dm
import src.managers.hash_manager as hm


class EndUI(QMainWindow):

    def __init__(self, sw: QStackedWidget):
        super(EndUI, self).__init__()
        self.sw = sw
        center = QLabel()
        center.setMinimumSize(960, 480)
        self.setCentralWidget(center)

        label = QLabel(cm.tr().end.label)
        label.setObjectName("big")
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_drop = QPushButton(cm.tr().end.button_drop)
        button_drop.clicked.connect(lambda: self.sw.switch_to_drop())
        button_output = QPushButton(cm.tr().end.button_output)
        button_output.clicked.connect(lambda: os.startfile(str(cm.get_temp_output_folder()).replace("/", "\\")))
        for i in [button_drop, button_output]:
            button_layout.addWidget(i)

        spacer = QFrame()
        spacer.setMinimumHeight(100)

        layout.addWidget(spacer)
        layout.addLayout(button_layout)
        center.setLayout(layout)

        css = ["drop.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))
