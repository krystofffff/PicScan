from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGraphicsScene, \
    QGraphicsPixmapItem
from src.operations import graphicOperations as Go
import src.managers.dataManager as Dm
from src.controllers.edit.editController import EditView


class ImageDialog(QDialog):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx
        self.setWindowTitle("image")

        pic = QGraphicsPixmapItem()
        pixmap = Go.get_qpixmap(Dm.get_cutouts()[self.idx].img)
        pic.setPixmap(pixmap)

        self.scene = QGraphicsScene()
        self.scene.addItem(pic)
        self.graphicsView = EditView(self.scene)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.graphicsView)
        self.setLayout(self.layout)

        self.exec_()

