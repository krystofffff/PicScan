from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

import graphicOperations as Go
import dataManager as Dm


class Dialog(QDialog):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx
        self.setWindowTitle("image")
        image = Go.get_qpixmap(Dm.get_cutouts()[self.idx].img)
        downscaled_image = image.scaled(1000, 800, Qt.KeepAspectRatio)

        label = QLabel()
        label.setPixmap(downscaled_image)
        label.setMinimumSize(label.sizeHint())

        vbox = QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)
        self.exec_()
