from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy
from src.utils import graphic_utils as gra
import src.managers.data_manager as dm
from src.controllers.image_dialog import ImageDialog


class MainLabel(QLabel):

    def __init__(self, parent, idx):
        QLabel.__init__(self, parent)
        self.idx = idx
        self.pixmap = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.update_pixmap()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        self.setFixedHeight(self.width())
        scaled_size = self.size()
        scaled_size.scale(self.size(), Qt.KeepAspectRatio)
        if not self.pixmap or scaled_size != self.pixmap.size():
            self._update_label()

    def _set_scaled_pixmap(self, pixmap):
        self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _update_label(self):
        self.setPixmap(self.pixmap.scaled(
            self.size(), Qt.KeepAspectRatio,
            Qt.SmoothTransformation))

    def rotate_cutout(self):
        dm.rotate_cutout(self.idx)
        self.update_pixmap()

    def toggle_cutout(self):
        dm.toggle_cutout(self.idx)
        self.update_pixmap()

    def update_pixmap(self):
        co = dm.get_cutouts()[self.idx]
        if co.enabled:
            self.pixmap = gra.get_qpixmap(co.img)
        else:
            self.pixmap = gra.get_qpixmap(co.disabled_img)
        self._set_scaled_pixmap(self.pixmap)

    def mousePressEvent(self, event):
        img = dm.get_cutouts()[self.idx].img
        ImageDialog(img)
