from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, Qt
from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QGridLayout, QPushButton, \
    QSizePolicy, QFrame, QMainWindow

from definitions import ROOT_DIR, CSS_DIR
from src.controllers.edit.editController import EditUi
from src.controllers.mainLabel import MainLabel
from src.controllers.popupDialog import PopupDialog
from src.managers import dataManager as Dm
from src.utils import graphicUtils as Gra


class MainUi(QMainWindow):
    progress = pyqtSignal(bool)

    def __init__(self, sw):
        super(MainUi, self).__init__()

        self.sw = sw
        self.center = QWidget()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
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

        self.next_button = QPushButton("NEXT")
        self.next_button.clicked.connect(lambda: self.switch_to_progress(False))
        self.auto_button = QPushButton("AUTO")
        self.auto_button.clicked.connect(lambda: self.switch_to_progress(True))
        self.quit_button = QPushButton("QUIT")
        self.quit_button.clicked.connect(lambda: self._switch_to_drop())
        for i in [self.next_button, self.auto_button, self.quit_button]:
            i.setMinimumSize(80, 20)
            i.setMaximumSize(160, 40)
            self.buttons_h_layout.addWidget(i)

        self.icons = {x: QIcon(ROOT_DIR + f"/assets/{x}.png") for x in ["rem", "rot", "edit"]}

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
            if PopupDialog("Start auto mode ?").exec_():
                Dm.save_cutouts()
                self.progress.emit(True)
                self.sw.setCurrentIndex(1)
        else:
            self.progress.emit(False)
            self.sw.setCurrentIndex(1)

    @pyqtSlot()
    def load_new_image(self):
        self._clear_scroll_area()
        self.scroll_area.verticalScrollBar().minimum()
        self.file_name_label.setText(Dm.get_file_name())
        _COLUMN_COUNT = 2
        for i in range(len(Dm.get_cutouts())):
            layout = self._build_item(self.scroll_area, i)
            x, y = i % _COLUMN_COUNT, i // _COLUMN_COUNT
            self.grid_layout.addLayout(layout, y, x)
        # TODO is there need for self.pixmap ?
        self.pixmap = Gra.get_qpixmap(Dm.get_canvas())
        self.canvas.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.canvas.setAlignment(Qt.AlignCenter)
        self.update_label()

    def resizeEvent(self, event: QResizeEvent):
        scaled_size = self.canvas.size()
        scaled_size.scale(self.canvas.size(), Qt.KeepAspectRatio)
        self.update_label(event)

    def update_label(self, event=None):
        self.canvas.setPixmap(self.pixmap.scaled(self.canvas.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _build_item(self, parent, idx):
        h_layout = QHBoxLayout()
        frame = QFrame()
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        label = MainLabel(parent, idx)
        rot_button = self._build_rotate_button(25, label)
        edi_button = self._build_edit_button(25, idx, label)
        rem_button = self._build_remove_button(25, label)
        for i in [rot_button, edi_button, rem_button]:
            v_layout.addWidget(i)
        h_layout.addWidget(label, 9)
        h_layout.addWidget(frame, 1)
        return h_layout

    def _build_button(self, size, icon_path):
        button = QPushButton()
        button.setFixedSize(size, size)
        button.setIcon(self.icons[icon_path])
        icon_size = size - 5
        button.setIconSize(QSize(icon_size, icon_size))
        return button

    def _build_remove_button(self, size, label):
        button = self._build_button(size, "rem")
        button.clicked.connect(lambda: label.toggle_cutout())
        return button

    def _build_rotate_button(self, size, label):
        button = self._build_button(size, "rot")
        button.clicked.connect(lambda: label.rotate_cutout())
        return button

    def _build_edit_button(self, size, idx, label):
        button = self._build_button(size, "edit")
        button.clicked.connect(lambda: self._open_edit(idx, label))
        return button

    def _open_edit(self, idx, label):
        # TODO should be persistent ? (+ sw indexing ?)
        EditUi(self.sw, idx, label, Dm.get_canvas())

    def _switch_to_drop(self):
        Dm.clear_data()
        self.sw.setCurrentIndex(0)
        self._clear_scroll_area()
