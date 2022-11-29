from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QHBoxLayout, \
    QMainWindow, QVBoxLayout, QPushButton, QGraphicsPixmapItem
from PyQt5.QtCore import Qt

import graphicOperations as Go
import geometricOperations as Geo
import dataManager as Dm
from selectionBoxClass import SelectionBox


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

        self.graphicsView = QGraphicsView()

        self.scene = QGraphicsScene()
        pic = QGraphicsPixmapItem()
        pixmap = Go.get_qpixmap(canvas)
        pic.setPixmap(pixmap)
        w, h = pixmap.width(), pixmap.height()
        self.scene.setSceneRect(0, 0, w, h)
        self.scene.addItem(pic)
        self.scene.setBackgroundBrush(QColor(150, 150, 150))

        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.graphicsView.setAlignment(Qt.AlignCenter | Qt.AlignCenter)

        self.mainHLayout.addWidget(self.graphicsView, 9)

        self.points = [x[0] for x in Dm.get_cutout_points(self.idx)]

        self.selectionBox = SelectionBox(self.scene, self.points)

        self.barFrame = QWidget()
        self.mainHLayout.addWidget(self.barFrame, 1)
        self.verticalBar = QVBoxLayout()
        self.verticalBar.setAlignment(Qt.AlignBottom)
        self.barFrame.setLayout(self.verticalBar)

        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(lambda: self._reset_selection_box())
        self.acceptButton = QPushButton("Ok")
        self.acceptButton.clicked.connect(lambda: self._accept_selection())
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

    def resizeEvent(self, event):
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
    #     for i in [self.resetButton, self.acceptButton]:
    #         i.setFixedHeight(i.width())
