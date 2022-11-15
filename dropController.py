import os
import tkinter.filedialog
from tkinter import filedialog

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QFileDialog
import dataManager as Dm


class DropUi(QMainWindow):
    def __init__(self, sw, main):
        super(DropUi, self).__init__()

        self.sw = sw
        self.main = main
        self.center = QLabel()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)
        self.setAcceptDrops(True)
        self.label = QLabel("Drag & Drop")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(200, 50)
        self.label2 = QLabel("or")
        self.label2.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.center.setLayout(self.layout)

        self.browserButton = QPushButton("Choose file")
        self.browserButton.clicked.connect(lambda: self.openFileExplorer())
        self.browserButton.setObjectName("browserButton")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.browserButton)
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

    def openFileExplorer(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file')
        arrUrls = []
        for url in fname[0]:
            arrUrls.append(QUrl('file:///' + url))
        if fname == ([], ''):  # if cancel is pressed prevents from sending empty string further
            return
        Dm.addFile(arrUrls)
        self.main.loadNewImage()
        self.sw.setCurrentIndex(0)
        self.label.setText("Drag & Drop")
