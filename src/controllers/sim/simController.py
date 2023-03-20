import pickle
import sys
import tracemalloc

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QGridLayout, QPushButton, \
    QSizePolicy, QFrame, QMainWindow
from PyQt5.QtCore import QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

from src.controllers.popupDialog import PopupDialog
from src.controllers.sim.simItem import SimItem
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
        self.next_button.clicked.connect(lambda: self.process(True))
        self.auto_button = QPushButton("DECLINE")
        self.auto_button.clicked.connect(lambda: self.process(False))
        for i in [self.next_button, self.auto_button]:
            i.setMinimumSize(80, 20)
            i.setMaximumSize(160, 40)
            self.buttons_h_layout.addWidget(i)

        SimItem.icons = {x: QIcon(ROOT_DIR + f"/assets/{x}.png") for x in ["rem", "swap"]}

        css = ["main.css", "buttons.css", "sim.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def process(self, is_accepted):
        Hm.process_hash_images(is_accepted)
        if Hm.is_empty():
            self.sw.setCurrentIndex(4)
        else:
            self.load_new_image()

    def _clear_scroll_area(self):
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(0).layout()
            label = item.itemAt(0).widget()
            frame = item.itemAt(1).widget()
            vbox = frame.layout()
            for j in range(vbox.count()):
                vbox.itemAt(0).widget().setParent(None)
            [x.setParent(None) for x in [vbox, frame, label, item]]

    @pyqtSlot()
    def load_new_image(self, h=None):
        self._clear_scroll_area()
        _COLUMN_COUNT = 2
        Hm.build_new_hashimages(h)
        hash_images = Hm.get_hashimages()
        for idx, hash_image in enumerate(hash_images[1:]):
            layout = SimItem(self.scroll_area, idx, hash_image, self)
            x, y = idx % _COLUMN_COUNT, idx // _COLUMN_COUNT
            self.grid_layout.addLayout(layout, y, x)
        self.pixmap = Gra.get_qpixmap(hash_images[0].img)
        self.canvas.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.canvas.setAlignment(Qt.AlignCenter)
        self.update_label()
        self.scroll_area.verticalScrollBar().setValue(0)

    def resizeEvent(self, event):
        self.update_label()

    def showEvent(self, event):
        self.update_label()

    def update_label(self):
        self.canvas.setPixmap(self.pixmap.scaled(self.canvas.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
