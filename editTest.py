import sys

import cv2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QWidget, QHBoxLayout, \
    QMainWindow, QVBoxLayout, QPushButton, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF, QRect, QRectF

import graphicOperations
from SelectionBox import SelectionBox


class EditUI(QMainWindow):
    def __init__(self):
        super(EditUI, self).__init__()

        self.center = QWidget()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)
        self.mainHLayout = QHBoxLayout()
        self.center.setLayout(self.mainHLayout)

        self.scene = QGraphicsScene()
        pic = QGraphicsPixmapItem()
        self.pixmap = graphicOperations.getQPixmap(cv2.imread("./tests/testingImages/output.jpg"))
        pic.setPixmap(self.pixmap)
        w, h = self.pixmap.width(), self.pixmap.height()
        self.scene.setSceneRect(0, 0, h, w)
        self.scene.addItem(pic)
        self.graphicsView = QGraphicsView(self.scene)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.fitInView(self.scene.sceneRect())
        self.mainHLayout.addWidget(self.graphicsView, 9)
        self.graphicsView.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.selectionBox = SelectionBox(self.scene)

        self.barFrame = QWidget()
        self.mainHLayout.addWidget(self.barFrame, 1)
        self.verticalBar = QVBoxLayout()
        self.verticalBar.setAlignment(Qt.AlignBottom)
        self.barFrame.setLayout(self.verticalBar)

        self.resetButton = QPushButton("Reset")
        self.acceptButton = QPushButton("Ok")
        for i in [self.resetButton, self.acceptButton]:
            i.setFixedHeight(50)
            self.verticalBar.addWidget(i)

        self.setStyleSheet(open('css/edit.css').read())

    def resizeEvent(self, event):
        for i in [self.resetButton, self.acceptButton]:
            i.setFixedHeight(i.width())


app = QApplication(sys.argv)
view = EditUI()
view.show()
sys.exit(app.exec_())
