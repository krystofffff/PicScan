from PyQt5.QtGui import QMovie, QPen, QBrush, QColor, QPaintEvent, QPainter, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QCheckBox, QMessageBox, QHBoxLayout, QWidget, \
    QFrame
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog
import src.managers.dataManager as Dm
import src.managers.configManager as Cm
import src.controllers.configController as Sc
from definitions import ROOT_DIR, CSS_DIR
from src.controllers.drop.toggleClass import ToggleSwitch


class DropUi(QMainWindow):
    progress = pyqtSignal(bool)

    def __init__(self, sw):
        super(DropUi, self).__init__()

        self.sw = sw
        center = QLabel()
        center.setObjectName("outer")
        center.setMinimumSize(960, 480)
        self.setCentralWidget(center)
        self.setAcceptDrops(True)

        lay_h = QHBoxLayout()
        center.setLayout(lay_h)
        fr = QFrame()
        lay_h.addStretch()
        lay_h.addWidget(fr)
        lay_h.addStretch()

        self.label_1 = QLabel("Drag & Drop")
        self.label_1.setObjectName("big")
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel("or")
        self.label_2.setObjectName("big")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        fr.setLayout(self.layout)

        self.browser_button = QPushButton("Choose file")
        self.browser_button.clicked.connect(lambda: self.open_file_explorer())
        self.browser_button.setObjectName("browserButton")
        self.settings_button = QPushButton("Settings")
        self.settings_button.setMinimumWidth(200)
        self.settings_button.clicked.connect(lambda: Sc.ConfigDialog(self))

        self.ll = QHBoxLayout()
        self.checkbox = ToggleSwitch()
        self.checkbox.setFixedSize(100, 60)
        self.ll.addWidget(self.settings_button)
        self.ll.addWidget(self.checkbox)

        self.layout.addWidget(self.label_1)
        self.layout.addWidget(self.label_2)
        self.layout.addWidget(self.browser_button)
        self.layout.addLayout(self.ll)


        self._build_loading()
        self.stop_nn_loading(not Cm.get_nn_loading())

        css = ["drop.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def _build_loading(self):
        self.loading_container = QFrame(self)
        self.loading_container.setFixedSize(150, 50)
        layout_loading = QHBoxLayout(self.loading_container)
        layout_loading.setContentsMargins(0, 0, 0, 0)
        self.movie = QMovie("assets/spinner.gif")
        loading = QLabel()
        loading.setStyleSheet("font-size:14px;")
        loading.setFixedSize(50, 50)
        loading.setScaledContents(True)
        loading.setMovie(self.movie)
        loading_message = QLabel("AI is loading")
        layout_loading.addWidget(loading)
        layout_loading.addWidget(loading_message)
        self.loading_container.move(50, 50)

    def _set_input_enabled(self, val):
        self.browser_button.setEnabled(val)
        message = None if val else "AI is loading"
        self.browser_button.setToolTip(message)
        self.setAcceptDrops(val)

    @pyqtSlot(bool)
    def stop_nn_loading(self, val):
        if val:
            self.movie.stop()
        else:
            self.movie.start()
        self.loading_container.setVisible(not val)
        self._set_input_enabled(val)

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
        self.progress.emit(self.checkbox.isChecked())
        self.label_1.setText("Drag & Drop")
        event.accept()

    def open_file_explorer(self):
        file_name = QFileDialog.getOpenFileNames(self, 'Open file')[0]
        if not file_name:
            return
        Dm.set_file_count(file_name)
        Dm.add_file(file_name)
        self.progress.emit(self.checkbox.isChecked())
        self.label_1.setText("Drag & Drop")
