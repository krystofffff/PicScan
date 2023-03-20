from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsView


class EditView(QGraphicsView):

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setInteractive(True)

    def wheelEvent(self, event):
        factor = 1.1
        if event.angleDelta().y() < 0:
            factor = 0.9
        self.update_view(factor, event)

    def update_view(self, factor, event=None):
        if event is None:
            view_pos = QPoint(0, 0)
        else:
            view_pos = event.pos()
        scene_pos = self.mapToScene(view_pos)
        self.centerOn(scene_pos)
        self.scale(factor, factor)
        delta = self.mapToScene(view_pos) - self.mapToScene(self.viewport().rect().center())
        self.centerOn(scene_pos - delta)
