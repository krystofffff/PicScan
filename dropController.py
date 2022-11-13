from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QFileDialog
import dataManager as Dm


class DropUi(QtWidgets.QMainWindow):
    def __init__(self, sw, main):
        super(DropUi, self).__init__()
        uic.loadUi('uis/drop.ui', self)
        self.sw = sw
        self.main = main
        self.setFixedSize(self.size())
        self.setAcceptDrops(True)
        self.label = self.findChild(QtWidgets.QLabel, 'labelDrop')
        self.label2 = self.findChild(QtWidgets.QLabel, 'labelDrop_2')
        self.browserButton = self.findChild(QtWidgets.QPushButton, 'browserButton')
        self.browserButton.clicked.connect(lambda: self.openFileExplorer())
        self.fileDirComboBox = self.findChild(QtWidgets.QComboBox, 'comboBox')
        self.comboChange = [1]
        self.fileDirComboBox.currentIndexChanged.connect(lambda: self.selectionChange())
        self.setStyleSheet(open('css/drop.css').read())

    def dragEnterEvent(self, event):
        self.label.setText("Drop it here")
        event.accept()

    def dragLeaveEvent(self, event):
        self.label.setText("Drag & Drop")
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        urls = event.mimeData().urls()
        Dm.addFile(urls)
        self.main.loadNewImage()
        self.sw.setCurrentIndex(0)
        self.label.setText("Drag & Drop")
        event.accept()

    def selectionChange(self):
        if(self.comboChange[0]==1):
            self.comboChange[0] = 2
        else:
            self.comboChange[0] = 1

    def openFileExplorer(self):
        if (self.comboChange[0] == 1): #checks which comboBox index is active File(s) or Dir
            fname = QFileDialog.getOpenFileNames(self, 'Open file')
            arrUrls = []
            for url in fname[0]:
                arrUrls.append(QUrl('file:///' + url))
            if fname == ([], ''):  # if cancel is pressed prevents from sending empty string further
                return
            Dm.addFile(arrUrls)
            self.main.loadNewImage()
            self.sw.setCurrentIndex(0)

        elif(self.comboChange[0] == 2):
            dirname = QFileDialog.getExistingDirectoryUrl(self, 'Open directory')
            dirUrl = [dirname]
            if dirname.isEmpty():  # if cancel is pressed prevents from sending empty string further
                return
            Dm.addFile(dirUrl)
            self.main.loadNewImage()
            self.sw.setCurrentIndex(0)
