from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QFileDialog
import src.dataManager as Dm
import src.controllers.settingsController as sC


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

        self.browser_button = QPushButton("Choose file")
        self.browser_button.clicked.connect(lambda: self.open_file_explorer())
        self.browser_button.setObjectName("browserButton")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.browser_button)
        self.setStyleSheet(open('css/drop.css').read())

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: sC.SettingsDialog())
        self.layout.addWidget(self.settings_button)

    def dragEnterEvent(self, event):
        self.label.setText("Drop it here")
        event.accept()

    def dragLeaveEvent(self, event):
        self.label.setText("Drag & Drop")
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        urls = event.mimeData().urls()
        Dm.add_file(urls)
        self.main.load_new_image()
        self.sw.setCurrentIndex(0)
        self.label.setText("Drag & Drop")
        event.accept()

    def open_file_explorer(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file')
        arrUrls = []
        for url in fname[0]:
            arrUrls.append(QUrl('file:///' + url))
        if fname == ([], ''):
            return
        Dm.add_file(arrUrls)
        self.main.load_new_image()
        self.sw.setCurrentIndex(0)
        self.label.setText("Drag & Drop")
