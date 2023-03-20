from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QPushButton, QBoxLayout

from definitions import ROOT_DIR
from src.controllers.edit.editController import EditUi
from src.controllers.main.mainLabel import MainLabel
import src.managers.dataManager as Dm


class MainItem(QHBoxLayout):
    icons: dir

    def __init__(self, sw, parent, idx):
        super().__init__()
        self.sw = sw
        frame = QFrame()
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        label = MainLabel(parent, idx)

        rot_button = self._build_rotate_button(25, label)
        edi_button = self._build_edit_button(25, idx, label)
        rem_button = self._build_remove_button(25, label)
        for i in [rot_button, edi_button, rem_button]:
            v_layout.addWidget(i)
        self.addWidget(label, 9)
        self.addWidget(frame, 1)

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

    def _build_button(self, size, icon_path):
        button = QPushButton()
        button.setFixedSize(size, size)
        button.setIcon(self.icons[icon_path])
        icon_size = size - 5
        button.setIconSize(QSize(icon_size, icon_size))
        return button

    def _open_edit(self, idx, label):
        # TODO should be persistent ? (+ sw indexing ?) (Yeah probably should)
        EditUi(self.sw, idx, label, Dm.get_canvas())
