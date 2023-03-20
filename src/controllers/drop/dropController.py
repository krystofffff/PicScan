from PyQt5.QtGui import QMovie, QPen, QBrush, QColor, QPaintEvent, QPainter, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QCheckBox, QMessageBox, QHBoxLayout, QWidget, \
    QFrame
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog
import src.managers.dataManager as Dm
import src.managers.configManager as Cm
import src.managers.nnRotManager as Nm
import src.controllers.configController as Sc
from definitions import ROOT_DIR, CSS_DIR
from src.controllers.drop.toggleClass import ToggleSwitch
from src.controllers.popupDialog import PopupDialog


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

        self.browser_button = QPushButton("Choose files")
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

        self._build_folder_message()

        self.layout.addLayout(self.ll)

        self._build_loading()
        self.stop_nn_loading(not Cm.get_nn_loading())

        css = ["drop.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def _build_folder_message(self):
        self.folder_label = QLabel("Output folder doesn't exist")
        self.folder_label.setObjectName("folder_message")
        self.folder_label.setAlignment(Qt.AlignHCenter)
        self.update_output_folder_message()
        self.layout.addWidget(self.folder_label)

    @pyqtSlot()
    def update_output_folder_message(self):
        state = Cm.output_folder_exists()
        self.folder_label.setVisible(not state)
        self._update_inputs()

    def _build_loading(self):
        self.loading_container = QFrame(self)
        self.loading_container.setFixedSize(150, 50)
        layout_loading = QHBoxLayout(self.loading_container)
        layout_loading.setContentsMargins(0, 0, 0, 0)
        self.movie = QMovie("assets/spinner.gif")
        loading = QLabel()
        loading.setObjectName("loading")
        loading.setFixedSize(50, 50)
        loading.setScaledContents(True)
        loading.setMovie(self.movie)
        loading_message = QLabel("AI is loading")
        layout_loading.addWidget(loading)
        layout_loading.addWidget(loading_message)
        self.loading_container.move(50, 50)

    def _update_inputs(self):
        nn_ready = (Cm.get_nn_loading() and Nm.is_model_loaded()) or not Cm.get_nn_loading()
        val = Cm.output_folder_exists() and nn_ready
        self.browser_button.setEnabled(val)
        self.setAcceptDrops(val)

    @pyqtSlot(bool)
    def stop_nn_loading(self, val):
        if val:
            self.movie.stop()
        else:
            self.movie.start()
        self.loading_container.setVisible(not val)
        self._update_inputs()

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
        if Dm.get_file_count() > 0:
            Dm.add_file(urls_clean)
            self.progress.emit(self.checkbox.isChecked())
        else:
            PopupDialog("No images found", yes_mess=None, no_mess="OK").exec_()
        self.label_1.setText("Drag & Drop")
        event.accept()

    def open_file_explorer(self):
        file_name = QFileDialog.getOpenFileNames(self, 'Open file')[0]
        if file_name:
            Dm.set_file_count(file_name)
            if Dm.get_file_count() > 0:
                Dm.add_file(file_name)
                self.progress.emit(self.checkbox.isChecked())
            else:
                PopupDialog("No images found", yes_mess=None, no_mess="OK").exec_()
