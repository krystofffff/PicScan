from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QLabel, QVBoxLayout

from definitions import CSS_DIR


class EndUI(QMainWindow):

    def __init__(self, sw: QStackedWidget):
        super(EndUI, self).__init__()
        self.sw = sw
        self.center = QLabel()
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)

        self.label = QLabel("The End")
        self.label.setObjectName("big")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.setAlignment(Qt.AlignCenter)

        self.center.setLayout(self.layout)

        css = ["drop.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))
