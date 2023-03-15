from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGraphicsScene, \
    QGraphicsPixmapItem
from src.utils import graphicUtils as Gra
import src.managers.dataManager as Dm
from src.controllers.edit.editController import EditView


class ImageDialog(QDialog):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("image")

        pic = QGraphicsPixmapItem()
        pixmap = Gra.get_qpixmap(image)
        pic.setPixmap(pixmap)

        self.scene = QGraphicsScene()
        self.scene.addItem(pic)
        self.graphicsView = EditView(self.scene)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.graphicsView)
        self.setLayout(self.layout)

        self.exec_()

