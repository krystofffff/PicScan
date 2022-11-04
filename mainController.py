from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
import dataManager as Dm
import graphicOperations as Go


class MainUi(QtWidgets.QMainWindow):

    def __init__(self, sw):
        super(MainUi, self).__init__()
        uic.loadUi('uis/main.ui', self)
        self.sw = sw
        self.setFixedSize(self.size())
        self.canvas = self.findChild(QtWidgets.QLabel, 'canvas')
        self.urlTextField = self.findChild(QtWidgets.QLineEdit, 'dirTextField')
        self.scrollArea = self.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self.layout = self.findChild(QtWidgets.QGridLayout, 'gridLayout_2')
        self.saveButton = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.saveButton.clicked.connect(lambda: self.saveImages())
        self.nextButton = self.findChild(QtWidgets.QPushButton, 'nextButton')
        self.nextButton.clicked.connect(lambda: self.loadNewImage())
        self.endButton = self.findChild(QtWidgets.QPushButton, 'endButton')
        self.endButton.clicked.connect(lambda: self.switchToDrop())
        self.setStyleSheet(open('css/main.css').read())

    def __clearScrollArea(self):
        for i in reversed(range(self.layout.count())):
            a = self.layout.itemAt(i)
            for j in reversed(range(a.layout().count())):
                a.layout().itemAt(j).widget().deleteLater()
            a.layout().deleteLater()

    def loadNewImage(self):
        Dm.loadNewCanvas()
        Dm.generateCutouts()
        self.nextButton.setEnabled(not Dm.isEmpty())
        self.scrollArea.verticalScrollBar().minimum()
        # TODO check deletion
        self.__clearScrollArea()
        for idx, i in enumerate(Dm.getCutouts()):
            layout = self.__buildItem(idx, i)
            x, y = idx % 2, idx // 2
            self.layout.addLayout(layout, y, x)
        scaled = Go.resizeImageToFit(Dm.getCanvas(), self.canvas.size())
        self.canvas.setPixmap(Go.getQPixmap(scaled))

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
        Dm.getCutouts()[idx] = Go.rotateImage(Dm.getCutouts()[idx])
        scaled = Go.resizeImageToFit(Dm.getCutouts()[idx], label.size())
        label.setPixmap(Go.getQPixmap(scaled))

    def saveImages(self):
        Dm.saveCutouts()

    def switchToDrop(self):
        Dm.clearData()
        self.sw.setCurrentIndex(1)
