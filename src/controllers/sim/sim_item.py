from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QLabel, QPushButton, QSizePolicy

from src.controllers.sim.sim_label import SimLabel


class SimItem(QHBoxLayout):
    icons: dir

    def __init__(self, parent, idx, hash_image, sim):
        super().__init__()

        self.sim = sim
        frame = QFrame()
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        label = SimLabel(parent, idx, hash_image)
        v_layout.addWidget(label)
        perc = QLabel(f"{hash_image.sim * 100: .0f} %")
        perc.setObjectName("perc")
        perc.setMaximumSize(200, 50)
        edi_button = self._build_swap_button(30, hash_image)
        rem_button = self._build_remove_button(30, label)
        for i in [perc, edi_button, rem_button]:
            v_layout.addWidget(i)
        self.addWidget(label, 9)
        self.addWidget(frame, 1)

    def _build_button(self, size, icon_path):
        button = QPushButton()
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setSizePolicy(sp)
        button.setMaximumSize(200, 50)
        button.setIcon(self.icons[icon_path])
        icon_size = size - 5
        button.setIconSize(QSize(icon_size, icon_size))
        return button

    def _build_remove_button(self, size, label):
        button = self._build_button(size, "rem")
        button.clicked.connect(lambda: label.toggle_sim())
        return button

    def _build_swap_button(self, size, hash_image):
        button = self._build_button(size, "swap")
        button.clicked.connect(lambda: self.sim.load_new_image(hash_image.h))
        return button
