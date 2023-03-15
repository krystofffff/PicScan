import random

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QGridLayout, QPushButton, \
    QSizePolicy, QFrame, QMainWindow
from PyQt5.QtCore import QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

from src.controllers.popupDialog import PopupDialog
from src.managers import dataManager as Dm
from src.utils import graphicUtils as Gra
from src.controllers.sim.simLabel import SimLabel
from definitions import ROOT_DIR, CSS_DIR
import src.managers.hashManager as Hm


class SimUI(QMainWindow):
    progress = pyqtSignal(bool)

    def __init__(self, sw):
        super(SimUI, self).__init__()

        self.sw = sw
        self.center = QWidget()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)
        self.main_h_layout = QHBoxLayout()
        self.center.setLayout(self.main_h_layout)
        self.canvas = QLabel()

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea(widgetResizable=True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.grid_layout = QGridLayout()
        self.scroll_inner_container = QWidget()
        self.scroll_inner_container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_inner_container)

        self.buttons_h_layout = QHBoxLayout()
        self.v_layout.addWidget(self.canvas, 9)
        self.v_layout.addLayout(self.buttons_h_layout, 1)

        self.temp = QWidget()
        self.temp.setLayout(self.v_layout)
        self.main_h_layout.addWidget(self.temp, 1)
        self.main_h_layout.addWidget(self.scroll_area, 2)

        self.next_button = QPushButton("ACCEPT")
        self.next_button.clicked.connect(lambda: self.switch_to_progress(False))
        self.auto_button = QPushButton("DECLINE")
        self.auto_button.clicked.connect(lambda: self.switch_to_progress(True))
        for i in [self.next_button, self.auto_button]:
            i.setMinimumSize(80, 20)
            i.setMaximumSize(160, 40)
            self.buttons_h_layout.addWidget(i)

        self.icons = {x: QIcon(ROOT_DIR + f"/assets/{x}.png") for x in ["rem", "swap"]}

        css = ["main.css", "buttons.css", "sim.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

        self.load_new_image()

    # TODO CHECK
    def _clear_scroll_area(self):
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(0).layout()
            label = item.itemAt(0).widget()
            frame = item.itemAt(1).widget()
            vbox = frame.layout()
            for j in range(vbox.count()):
                vbox.itemAt(0).widget().setParent(None)
            [x.setParent(None) for x in [vbox, frame, label, item]]

    def switch_to_progress(self, in_auto_mode):
        if PopupDialog("Start auto mode ?").exec_():
            Dm.save_cutouts()
            self.progress.emit(in_auto_mode)
            self.sw.setCurrentIndex(1)

    @pyqtSlot()
    def load_new_image(self):
        _COLUMN_COUNT = 2
        for idx, img in enumerate(Hm.load_imgs_for_simui_beta()[1:]):
            layout = self._build_item(self.scroll_area, idx, img)
            x, y = idx % _COLUMN_COUNT, idx // _COLUMN_COUNT
            self.grid_layout.addLayout(layout, y, x)
        # # # TODO is there need for self.pixmap ?
        self.pixmap = Gra.get_qpixmap(Hm.load_imgs_for_simui_beta()[0])
        self.canvas.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.canvas.setAlignment(Qt.AlignCenter)
        self.update_label()

    def resizeEvent(self, event):
        self.update_label()

    def showEvent(self, event):
        self.update_label()

    def update_label(self):
        self.canvas.setPixmap(self.pixmap.scaled(self.canvas.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _build_item(self, parent, idx, img):
        h_layout = QHBoxLayout()
        frame = QFrame()
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        label = SimLabel(parent, idx, img)
        v_layout.addWidget(label)
        perc = QLabel(f"{99-idx} %")
        perc.setObjectName("perc")
        perc.setMaximumSize(150, 50)
        edi_button = self._build_swap_button(30, idx, label)
        rem_button = self._build_remove_button(30, label)
        for i in [perc, edi_button, rem_button]:
            v_layout.addWidget(i)
        h_layout.addWidget(label, 9)
        h_layout.addWidget(frame, 1)
        return h_layout

    def _build_button(self, size, icon_path):
        button = QPushButton()
        button.setMaximumSize(50, 50)
        button.setIcon(self.icons[icon_path])
        icon_size = size - 5
        button.setIconSize(QSize(icon_size, icon_size))
        return button

    def _build_remove_button(self, size, label):
        button = self._build_button(size, "rem")
        # button.clicked.connect(lambda: label.toggle_cutout())
        return button

    def _build_swap_button(self, size, idx, label):
        button = self._build_button(size, "swap")
        # button.clicked.connect(lambda: self._open_edit(idx, label))
        return button
