import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame

from definitions import CSS_DIR
import src.managers.configManager as Cm


class EndUI(QMainWindow):

    def __init__(self, sw: QStackedWidget):
        super(EndUI, self).__init__()
        self.sw = sw
        center = QLabel()
        center.setMinimumSize(960, 480)
        self.setCentralWidget(center)

        label = QLabel("Finished")
        label.setObjectName("big")
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_drop = QPushButton("Back to Drop")
        button_drop.clicked.connect(lambda: sw.setCurrentIndex(0))
        button_output = QPushButton("Open output folder")
        button_output.clicked.connect(lambda: os.startfile(Cm.get_output_folder()))
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
