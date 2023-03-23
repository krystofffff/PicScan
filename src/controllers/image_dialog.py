from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGraphicsScene, \
    QGraphicsPixmapItem

from src.controllers.edit.edit_controller import EditView
from src.utils import graphic_utils as gra


class ImageDialog(QDialog):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("image")

        pic = QGraphicsPixmapItem()
        pixmap = gra.get_qpixmap(image)
        pic.setPixmap(pixmap)

        self.scene = QGraphicsScene()
        self.scene.addItem(pic)
        self.graphicsView = EditView(self.scene)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.graphicsView)
        self.setLayout(self.layout)

        self.exec_()

