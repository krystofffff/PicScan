from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy
import graphicOperations as Go
import dataManager as Dm


class Label(QLabel):
    def __init__(self, parent, img, idx):
        QLabel.__init__(self, parent)
        self.idx = idx
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.pixmap = Go.getQPixmap(img)
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
        co = Dm.getCutouts()[self.idx]
        if co.enabled:
            self.pixmap = Go.getQPixmap(co.img)
        else:
            self.pixmap = Go.getQPixmap(co.disabledImg)
        self.__setScaledPixmap(self.pixmap)
