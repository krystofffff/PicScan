from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QHBoxLayout, \
    QMainWindow, QVBoxLayout, QPushButton, QGraphicsPixmapItem, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint

from src.operations import graphicOperations as Go, geometricOperations as Geo
import src.managers.dataManager as Dm
from src.selectionBoxClass import SelectionBox


# TODO SPLIT IN SEPARATE FILES
class MainView(QGraphicsView):

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


class EditUi(QMainWindow):
    def __init__(self, sw, idx, label, canvas):
        super(EditUi, self).__init__()

        self.idx = idx
        self.label = label
        self.center = QWidget()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)
        self.mainHLayout = QHBoxLayout()
        self.center.setLayout(self.mainHLayout)

        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.clicked.connect(lambda: self.graphicsView.update_view(1.1))
        self.zoom_out_button = QPushButton("-")
        self.zoom_out_button.clicked.connect(lambda: self.graphicsView.update_view(0.9))
        self.select_button = QPushButton("Select\npoints")
        self.select_button.clicked.connect(lambda: self._select_points())
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(lambda: self.scene.reset_selection_box())
        self.accept_button = QPushButton("Ok")
        self.accept_button.clicked.connect(lambda: self._accept_selection())
        self.v_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.points = [x[0] for x in Dm.get_cutout_points(self.idx)]
        self.scene = MainScene(canvas, self.points, self.accept_button)
        self.graphicsView = MainView(self.scene)

        self.mainHLayout.addWidget(self.graphicsView, 9)
        self.barFrame = QWidget()
        self.mainHLayout.addWidget(self.barFrame, 1)
        self.verticalBar = QVBoxLayout()
        self.verticalBar.setAlignment(Qt.AlignBottom)
        self.barFrame.setLayout(self.verticalBar)

        for i in [self.zoom_in_button, self.zoom_out_button]:
            self.verticalBar.addWidget(i)
        self.verticalBar.addItem(self.v_spacer)
        for i in [self.select_button, self.reset_button, self.accept_button]:
            self.verticalBar.addWidget(i)

        self.sw = sw
        self.sw.addWidget(self)
        self.sw.setCurrentIndex(3)

        self.setStyleSheet(open('css/edit.css').read())

    def _accept_selection(self):
        p = Geo.get_corners_from_anchors(*self.scene.selection_box.get_points_from_anchors())
        Dm.update_cutout(self.idx, p)
        self.label.update_pixmap()
        self.sw.removeWidget(self)
        self.sw.setCurrentIndex(2)

    def _select_points(self):
        self.accept_button.setEnabled(False)
        self.scene.select_points()
