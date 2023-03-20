from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy
from src.utils import graphic_utils as gra
from src.controllers.image_dialog import ImageDialog


class SimLabel(QLabel):

    def __init__(self, parent, idx, hash_image):
        QLabel.__init__(self, parent)
        self.idx = idx
        self.hash_image = hash_image
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

    def toggle_sim(self):
        self.hash_image.toggle()
        self.update_pixmap()

    def update_pixmap(self):
        self.pixmap = gra.get_qpixmap(self.hash_image.get_img())
        self._set_scaled_pixmap(self.pixmap)

    def mousePressEvent(self, event):
        ImageDialog(self.hash_image.img)
