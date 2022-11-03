from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QFileDialog


class DropUi(QtWidgets.QMainWindow):
    def __init__(self, sw, dm, main):
        super(DropUi, self).__init__()
        uic.loadUi('uis/drop.ui', self)
        self.sw = sw
        self.dm = dm
        self.main = main
        self.setFixedSize(self.size())
        self.setAcceptDrops(True)
        self.label = self.findChild(QtWidgets.QLabel, 'labelDrop')
        self.label2 = self.findChild(QtWidgets.QLabel, 'labelDrop_2')
        self.browserButton = self.findChild(QtWidgets.QPushButton, 'browserButton')
        self.browserButton.clicked.connect(lambda: self.openFileExplorer())
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
        print(urls)
        self.dm.addFile(urls)
        self.main.setPath(self.dm.getNextImage())
        self.sw.setCurrentIndex(0)
        self.label.setText("Drag & Drop")
        event.accept()

    def openFileExplorer(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file')
        arrUrls = []
        for url in fname[0]:
            arrUrls.append(QUrl('file:///' + url))
        if fname == ([], ''):  # if cancel is pressed prevents from sending empty string further
            return
        self.dm.addFile(arrUrls)
        self.main.setPath(self.dm.getNextImage())
        self.sw.setCurrentIndex(0)
        self.label.setText("Drag & Drop")
