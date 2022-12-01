from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QHBoxLayout, \
    QMainWindow, QVBoxLayout, QPushButton, QGraphicsPixmapItem, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

import graphicOperations as Go
import geometricOperations as Geo
import dataManager as Dm
from selectionBoxClass import SelectionBox


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
        self.update_view(factor)

    def update_view(self, factor):
        view_pos = self.pos()
        scene_pos = self.mapToScene(view_pos)
        self.centerOn(scene_pos)
        self.scale(factor, factor)
        delta = self.mapToScene(view_pos) - self.mapToScene(self.viewport().rect().center())
        self.centerOn(scene_pos - delta)


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

        self.scene = QGraphicsScene()
        pic = QGraphicsPixmapItem()
        pixmap = Go.get_qpixmap(canvas)
        pic.setPixmap(pixmap)
        w, h = pixmap.width(), pixmap.height()
        off = 50
        self.scene.setSceneRect(-off, -off, w+2*off, h+2*off)
        self.scene.addItem(pic)
        self.scene.setBackgroundBrush(QColor(150, 150, 150))
        self.graphicsView = MainView(self.scene)

        self.mainHLayout.addWidget(self.graphicsView, 9)

        self.points = [x[0] for x in Dm.get_cutout_points(self.idx)]

        self.selectionBox = SelectionBox(self.scene, self.points)

        self.barFrame = QWidget()
        self.mainHLayout.addWidget(self.barFrame, 1)
        self.verticalBar = QVBoxLayout()
        self.verticalBar.setAlignment(Qt.AlignBottom)
        self.barFrame.setLayout(self.verticalBar)

        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.clicked.connect(lambda: self.graphicsView.update_view(1.1))
        self.zoom_out_button = QPushButton("-")
        self.zoom_out_button.clicked.connect(lambda: self.graphicsView.update_view(0.9))
        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(lambda: self._reset_selection_box())
        self.acceptButton = QPushButton("Ok")
        self.acceptButton.clicked.connect(lambda: self._accept_selection())
        self.v_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        for i in [self.zoom_in_button, self.zoom_out_button]:
            self.verticalBar.addWidget(i)
        self.verticalBar.addItem(self.v_spacer)
        for i in [self.resetButton, self.acceptButton]:
            self.verticalBar.addWidget(i)

        self.setStyleSheet(open('css/edit.css').read())

        self.sw = sw
        self.sw.addWidget(self)
        self.sw.setCurrentIndex(2)

    def _reset_selection_box(self):
        self.selectionBox.drop_all()
        self.selectionBox = SelectionBox(self.scene, self.points)

    def _accept_selection(self):
        p = Geo.get_corners_from_anchors(*self.selectionBox.get_points_from_anchors())
        Dm.update_cutout(self.idx, p)
        self.label.updatePixMap()
        self.sw.removeWidget(self)
        self.sw.setCurrentIndex(0)
