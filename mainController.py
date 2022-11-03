import cv2
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
import graphicOperations as Go


class MainUi(QtWidgets.QMainWindow):
    path = None
    canvasIMG = None

    def __init__(self, sw, dm):
        super(MainUi, self).__init__()
        uic.loadUi('uis/main.ui', self)
        self.sw = sw
        self.dm = dm
        self.setFixedSize(self.size())
        self.canvas = self.findChild(QtWidgets.QLabel, 'canvas')
        self.urlTextField = self.findChild(QtWidgets.QLineEdit, 'dirTextField')
        self.scrollArea = self.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self.layout = self.findChild(QtWidgets.QGridLayout, 'gridLayout_2')
        self.saveButton = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.saveButton.clicked.connect(lambda: self.saveImages())
        self.nextButton = self.findChild(QtWidgets.QPushButton, 'nextButton')
        self.nextButton.clicked.connect(lambda: self.setPath(self.dm.getNextImage()))
        self.endButton = self.findChild(QtWidgets.QPushButton, 'endButton')
        self.endButton.clicked.connect(lambda: self.switchToDrop())
        self.setStyleSheet(open('css/main.css').read())

    def setPath(self, path):
        if self.dm.isEmpty():
            self.nextButton.setEnabled(False)
        else:
            self.nextButton.setEnabled(True)
        self.path = path
        self.loadImage()

    def __clearScrollArea(self):
        for i in reversed(range(self.layout.count())):
            a = self.layout.itemAt(i)
            for j in reversed(range(a.layout().count())):
                a.layout().itemAt(j).widget().deleteLater()
            a.layout().deleteLater()

    def loadImage(self):
        self.scrollArea.verticalScrollBar().minimum()
        img, points = Go.findRectangles(Go.loadImage(self.path))
        self.dm.cutouts = Go.cutOutImages(img, points)
        # TODO check deletion
        self.__clearScrollArea()
        for idx, i in enumerate(self.dm.cutouts):
            layout = self.__buildItem(idx, i)
            x, y = idx % 2, idx // 2
            self.layout.addLayout(layout, y, x)
        self.canvasIMG = {
            "img": img
        }
        self.updateCanvasImage()

    def __buildItem(self, idx, img):
        h_layout = QtWidgets.QHBoxLayout()
        frame = QtWidgets.QFrame()
        v_layout = QtWidgets.QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 10, 0)
        label = QtWidgets.QLabel("l" + str(idx))
        label.setFixedSize(150, 150)
        label.setScaledContents(False)
        label.setAlignment(Qt.AlignCenter)
        label.setFrameStyle(1)
        scaled = Go.resizeImageToFit(img, label.size())
        label.setPixmap(Go.getQPixmap(scaled))
        button = QtWidgets.QPushButton()
        button.setFixedSize(25, 25)
        button.clicked.connect(lambda: self.__rotateCutout(idx, label))
        button.setIcon(QIcon("assets/rot.png"))
        button.setIconSize(QSize(20, 20))
        v_layout.addWidget(button)
        h_layout.addWidget(label)
        h_layout.addWidget(frame)
        return h_layout

    def __rotateCutout(self, idx, label):
        self.dm.cutouts[idx] = Go.rotateImage(self.dm.cutouts[idx])
        scaled = Go.resizeImageToFit(self.dm.cutouts[idx], label.size())
        label.setPixmap(Go.getQPixmap(scaled))

    def saveImages(self):
        for idx, img in enumerate(self.dm.cutouts):
            # TODO move to datamanager
            cv2.imwrite(("./output/img_" + str(idx) + ".jpg"), img)
        print("DONE")

    def getDir(self):
        url = QFileDialog.getOpenFileName(self, "Select Directory")[0]
        self.setPath(self=self, path=url)
        self.loadImage()

    def updateCanvasImage(self):
        scaled = Go.resizeImageToFit(self.canvasIMG["img"], self.canvas.size())
        self.canvas.setPixmap(Go.getQPixmap(scaled))

    def switchToDrop(self):
        self.dm.clearData()
        self.sw.setCurrentIndex(1)
