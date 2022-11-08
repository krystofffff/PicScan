from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
import dataManager as Dm
import graphicOperations as Go


class MainUi(QtWidgets.QMainWindow):

    buttonVisibility = False

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
        self.saveButton.clicked.connect(lambda: self.__saveImages())
        self.nextButton = self.findChild(QtWidgets.QPushButton, 'nextButton')
        self.nextButton.clicked.connect(lambda: self.loadNewImage())
        self.endButton = self.findChild(QtWidgets.QPushButton, 'endButton')
        self.endButton.clicked.connect(lambda: self.__switchToDrop())
        self.editButton = self.findChild(QtWidgets.QPushButton, 'editButton')
        self.editButton.clicked.connect(lambda: self.__switchButtonVisibility())
        self.setStyleSheet(open('css/main.css').read())

    def __switchButtonVisibility(self):
        self.buttonVisibility = not self.buttonVisibility
        for i in reversed(range(self.layout.count())):
            a = self.layout.itemAt(i)
            frame = a.layout().itemAt(1).widget()
            lay = frame.children()[0].layout()
            for j in reversed(range(lay.count())):
                lay.itemAt(j).widget().setVisible(self.buttonVisibility)

    def __clearScrollArea(self):
        # TODO CHECK DELETION
        for i in reversed(range(self.layout.count())):
            a = self.layout.itemAt(i)
            for j in reversed(range(a.layout().count())):
                a.layout().itemAt(j).widget().setParent(None)
            a.layout().setParent(None)

    def loadNewImage(self):
        Dm.loadNewCanvas()
        Dm.generateCutouts()
        self.nextButton.setEnabled(not Dm.isEmpty())
        self.scrollArea.verticalScrollBar().minimum()
        counter = 0
        for key, co in Dm.getCutouts().items():
            layout = self.__buildItem(self.scrollArea, counter, key, co)
            x, y = counter % 2, counter // 2
            counter += 1
            self.layout.addLayout(layout, y, x)
        scaled = Go.resizeImageToFit(Dm.getCanvas(), self.canvas.size())
        self.canvas.setPixmap(Go.getQPixmap(scaled))

    def __buildItem(self, parent, idx, key, img):
        h_layout = QtWidgets.QHBoxLayout()
        frame = QtWidgets.QFrame()
        v_layout = QtWidgets.QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        label = self.__buildLabel(parent, img)
        rot_button = self.__buildRotateButton(25, frame, idx, label)
        rem_button = self.__buildRemoveButton(25, h_layout, frame, key)
        buttons = [rot_button, rem_button]
        for i in buttons:
            v_layout.addWidget(i)
        h_layout.addWidget(label)
        h_layout.addWidget(frame)
        return h_layout

    def __buildLabel(self, parent, img):
        label = QtWidgets.QLabel(parent=parent)
        label.setFixedSize(150, 150)
        label.setScaledContents(False)
        label.setAlignment(Qt.AlignCenter)
        label.setFrameStyle(1)
        scaled = Go.resizeImageToFit(img, label.size())
        label.setPixmap(Go.getQPixmap(scaled))
        return label

    def __buildButton(self, size, parent, iconPath):
        button = QtWidgets.QPushButton(parent=parent)
        button.setFixedSize(size, size)
        button.setVisible(self.buttonVisibility)
        button.setIcon(QIcon(iconPath))
        icon_size = size - 5
        button.setIconSize(QSize(icon_size, icon_size))
        return button

    def __buildRemoveButton(self, size, top_parent, parent, key):
        button = self.__buildButton(size, parent, "assets/rem.png")
        button.clicked.connect(lambda: self.__removeCutout(top_parent, key))
        return button

    def __buildRotateButton(self, size, parent, idx, label):
        button = self.__buildButton(size, parent, "assets/rot.png")
        button.clicked.connect(lambda: self.__rotateCutout(idx, label))
        return button

    def __rotateCutout(self, idx, label):
        Dm.getCutouts()[idx] = Go.rotateImage(Dm.getCutouts()[idx])
        scaled = Go.resizeImageToFit(Dm.getCutouts()[idx], label.size())
        label.setPixmap(Go.getQPixmap(scaled))

    def __removeCutout(self, top_parent, key):
        Dm.removeCutout(key)
        a = top_parent
        for j in reversed(range(a.layout().count())):
            a.layout().itemAt(j).widget().setParent(None)
        a.layout().setParent(None)

    def __saveImages(self):
        Dm.saveCutouts()

    def __switchToDrop(self):
        Dm.clearData()
        self.buttonVisibility = False
        self.__clearScrollArea()
        self.sw.setCurrentIndex(1)
