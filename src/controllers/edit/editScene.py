from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
import src.operations.graphicOperations as Go
from src.controllers.edit.selectionBoxClass import SelectionBox


class MainScene(QGraphicsScene):

    def __init__(self, canvas, points, accept_button):
        super().__init__()
        pic = QGraphicsPixmapItem()
        pixmap = Go.get_qpixmap(canvas)
        pic.setPixmap(pixmap)
        w, h = pixmap.width(), pixmap.height()
        offset = 50
        self.setSceneRect(-offset, -offset, w + 2 * offset, h + 2 * offset)
        self.addItem(pic)
        self.setBackgroundBrush(QColor(150, 150, 150))
        self.points = points
        self.accept_button = accept_button
        self.selection_box = SelectionBox(self, self.points)

    def reset_selection_box(self):
        self.selection_box.drop_all()
        self.selection_box = SelectionBox(self, self.points)
        self.accept_button.setEnabled(self.selection_box.is_ready)

    def mousePressEvent(self, event):
        if not self.selection_box.is_ready:
            self.selection_box.add_anchor(event.scenePos().x(), event.scenePos().y())
            self.accept_button.setEnabled(self.selection_box.is_ready)
        else:
            super().mousePressEvent(event)

    def select_points(self):
        self.selection_box.drop_all()
        self.selection_box = SelectionBox(self, None)