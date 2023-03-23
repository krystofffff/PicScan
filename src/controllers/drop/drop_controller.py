from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFrame

import src.controllers.config_controller as cc
import src.managers.config_manager as cm
import src.managers.data_manager as dm
import src.managers.nn_rot_manager as nm
from definitions import CSS_DIR
from src.controllers.drop.toggle_widget import ToggleSwitch
from src.controllers.popup_dialog import PopupDialog


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

        self.label_1 = QLabel(cm.tr().drop.label_1)
        self.label_1.setObjectName("big")
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(cm.tr().drop.label_2)
        self.label_2.setObjectName("big")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        fr.setLayout(self.layout)

        self.browser_button = QPushButton(cm.tr().drop.browser_button)
        self.browser_button.clicked.connect(lambda: self.open_file_explorer())
        self.browser_button.setObjectName("browserButton")
        self.settings_button = QPushButton(cm.tr().drop.settings_button)
        self.settings_button.setMinimumWidth(200)
        self.settings_button.clicked.connect(lambda: cc.ConfigDialog(self))

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
        self.stop_nn_loading(not cm.get_nn_loading())

        css = ["drop.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def _build_folder_message(self):
        self.folder_label = QLabel(cm.tr().drop.folder_label)
        self.folder_label.setObjectName("folder_message")
        self.folder_label.setAlignment(Qt.AlignHCenter)
        self.update_output_folder_message()
        self.layout.addWidget(self.folder_label)

    @pyqtSlot()
    def update_output_folder_message(self):
        state = cm.output_folder_exists()
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
        loading_message = QLabel(cm.tr().drop.loading_message)
        layout_loading.addWidget(loading)
        layout_loading.addWidget(loading_message)
        self.loading_container.move(50, 50)

    def _update_inputs(self):
        nn_ready = (cm.get_nn_loading() and nm.is_model_loaded()) or not cm.get_nn_loading()
        val = cm.output_folder_exists() and nn_ready
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
        self.label_1.setText(cm.tr().drop.label_1_hover)
        event.accept()

    def dragLeaveEvent(self, event):
        self.label_1.setText(cm.tr().drop.label_1)
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        urls = event.mimeData().urls()
        urls_clean = []
        for i in urls:
            urls_clean.append(i.path()[1:])
        dm.set_file_count(urls_clean)
        self._start(urls_clean)
        self.label_1.setText(cm.tr().drop.label_1)
        event.accept()

    def open_file_explorer(self):
        file_name = QFileDialog.getOpenFileNames(self, cm.tr().drop.folder)[0]
        if file_name:
            dm.set_file_count(file_name)
            self._start(file_name)

    def _start(self, inp):
        if dm.get_file_count() > 0:
            dm.add_file(inp)
            self.progress.emit(self.checkbox.isChecked())
        else:
            PopupDialog(cm.tr().drop.popup_dialog, yes_mess=None, no_mess="OK").exec_()
