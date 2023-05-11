from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QGridLayout, QPushButton, \
    QSizePolicy, QMainWindow

from definitions import ROOT_DIR, CSS_DIR
from src.controllers.main.main_item import MainItem
from src.controllers.popup_dialog import PopupDialog
from src.managers import data_manager as dm
import src.managers.hash_manager as hm
import src.managers.config_manager as cm
from src.utils import graphic_utils as gra


class MainUi(QMainWindow):
    progress = pyqtSignal(bool)

    def __init__(self, sw):
        super(MainUi, self).__init__()

        self.sw = sw
        MainItem.icons = {x: QIcon(ROOT_DIR + f"/assets/{x}.png") for x in ["rem", "rot", "edit"]}
        self.center = QWidget()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
        self.pixmap = None
        self.setCentralWidget(self.center)
        self.main_h_layout = QHBoxLayout()
        self.center.setLayout(self.main_h_layout)
        self.canvas = QLabel()
        self.main_h_layout.addWidget(self.canvas, 5)
        self.v_layout = QVBoxLayout()
        self.main_h_layout.addLayout(self.v_layout, 5)
        self.scroll_area = QScrollArea(widgetResizable=True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.v_layout.addWidget(self.scroll_area, 9)
        self.grid_layout = QGridLayout()
        self.scroll_inner_container = QWidget()
        self.scroll_inner_container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_inner_container)
        self.buttons_h_layout = QHBoxLayout()
        self.file_name_label = QLabel()
        self.file_name_label.setAlignment(Qt.AlignCenter)
        self.v_layout.addWidget(self.file_name_label, 1)
        self.v_layout.addLayout(self.buttons_h_layout, 1)

        self.next_button = QPushButton(cm.tr().main.next_button)
        self.next_button.clicked.connect(lambda: self.switch_to_progress(False))
        self.auto_button = QPushButton(cm.tr().main.auto_button)
        self.auto_button.clicked.connect(lambda: self.switch_to_progress(True))

        for i in [self.next_button, self.auto_button]:
            i.setMinimumSize(80, 20)
            i.setMaximumSize(160, 40)
            self.buttons_h_layout.addWidget(i)

        css = ["main.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def _clear_scroll_area(self):
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(0).layout()
            label = item.itemAt(0).widget()
            frame = item.itemAt(1).widget()
            vbox = frame.layout()
            for j in range(vbox.count()):
                vbox.itemAt(0).widget().setParent(None)
            vbox.setParent(None)
            frame.setParent(None)
            label.setParent(None)
            item.setParent(None)

    def switch_to_progress(self, in_auto_mode):
        if in_auto_mode:
            if PopupDialog(cm.tr().main.popup_dialog).exec_():
                self.proceed(True)
        else:
            self.proceed(False)

    def proceed(self, in_auto_mode):
        retry = True
        while retry:
            retry = False
            success = dm.save_cutouts()
            if not success:
                retry = self.error_dialog()
                if not retry:
                    self.sw.switch_to_drop()
            else:
                self.progress.emit(in_auto_mode)

    def error_dialog(self):
        return PopupDialog(message=cm.tr().errors.missing_output_folder, no_mess=cm.tr().popup_dialog.ok,
                           yes_mess=cm.tr().popup_dialog.try_again).exec_()

    @pyqtSlot()
    def load_new_image(self):
        self._clear_scroll_area()
        self.scroll_area.verticalScrollBar().minimum()
        self.file_name_label.setText(dm.get_file_name())
        _COLUMN_COUNT = 2
        for i in range(len(dm.get_cutouts())):
            layout = MainItem(self.sw, self.scroll_area, i)
            x, y = i % _COLUMN_COUNT, i // _COLUMN_COUNT
            self.grid_layout.addLayout(layout, y, x)
        self.pixmap = gra.get_qpixmap(dm.get_canvas())
        self.canvas.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.canvas.setAlignment(Qt.AlignCenter)
        self.update_label()

    def showEvent(self, event):
        self.update_label()

    def resizeEvent(self, event: QResizeEvent):
        scaled_size = self.canvas.size()
        scaled_size.scale(self.canvas.size(), Qt.KeepAspectRatio)
        self.update_label()

    def update_label(self):
        self.canvas.setPixmap(self.pixmap.scaled(self.canvas.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
