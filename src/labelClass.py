from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy
from src.operations import graphicOperations as Go
import src.dataManager as Dm
from src.dialogClass import Dialog


class Label(QLabel):
    def __init__(self, parent, img, idx):
        QLabel.__init__(self, parent)
        self.idx = idx
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.pixmap = Go.get_qpixmap(img)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        self.setFixedHeight(self.width())
        scaledSize = self.size()
        scaledSize.scale(self.size(), Qt.KeepAspectRatio)
        if not self.pixmap or scaledSize != self.pixmap.size():
            self.updateLabel()

    def __setScaledPixmap(self, pixmap):
        self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def updateLabel(self):
        self.setPixmap(self.pixmap.scaled(
            self.size(), Qt.KeepAspectRatio,
            Qt.SmoothTransformation))

    def updatePixMap(self):
        co = Dm.get_cutouts()[self.idx]
        if co.enabled:
            self.pixmap = Go.get_qpixmap(co.img)
        else:
            self.pixmap = Go.get_qpixmap(co.disabled_img)
        self.__setScaledPixmap(self.pixmap)

    def mousePressEvent(self, event):
        Dialog(self.idx)
