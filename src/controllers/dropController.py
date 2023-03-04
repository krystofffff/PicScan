from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import src.managers.dataManager as Dm
import src.controllers.configController as Sc
from definitions import ROOT_DIR


class DropUi(QMainWindow):
    progress = pyqtSignal(bool)

    def __init__(self, sw):
        super(DropUi, self).__init__()

        self.sw = sw
        self.center = QLabel()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)
        self.setAcceptDrops(True)
        self.label_1 = QLabel("Drag & Drop")
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setFixedSize(200, 50)
        self.label_2 = QLabel("or")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.center.setLayout(self.layout)

        self.browser_button = QPushButton("Choose file")
        self.browser_button.clicked.connect(lambda: self.open_file_explorer())
        self.browser_button.setObjectName("browserButton")

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: Sc.ConfigDialog())

        for i in [self.label_1, self.label_2, self.browser_button, self.settings_button]:
            self.layout.addWidget(i)

        self.setStyleSheet(open(ROOT_DIR + '/css/drop.css').read())

    def dragEnterEvent(self, event):
        self.label_1.setText("Drop it here")
        event.accept()

    def dragLeaveEvent(self, event):
        self.label_1.setText("Drag & Drop")
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        urls = event.mimeData().urls()
        urls_clean = []
        for i in urls:
            urls_clean.append(i.path()[1:])
        Dm.set_file_count(urls_clean)
        Dm.add_file(urls_clean)
        self.progress.emit(False)
        self.sw.setCurrentIndex(1)
        self.label_1.setText("Drag & Drop")
        event.accept()

    def open_file_explorer(self):
        file_name = QFileDialog.getOpenFileNames(self, 'Open file')[0]
        if not file_name:
            return
        Dm.set_file_count(file_name)
        Dm.add_file(file_name)
        self.sw.setCurrentIndex(1)
        self.progress.emit(False)
        self.label_1.setText("Drag & Drop")
