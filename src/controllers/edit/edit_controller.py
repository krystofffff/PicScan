from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, \
    QMainWindow, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy

import src.managers.data_manager as dm
import src.managers.config_manager as cm
from definitions import CSS_DIR
from src.controllers.edit.edit_scene import MainScene
from src.controllers.edit.edit_view import EditView
from src.utils import geometric_utils as geo


class EditUi(QMainWindow):
    def __init__(self, sw, idx, label, canvas):
        super(EditUi, self).__init__()

        self.idx = idx
        self.label = label
        self.center = QWidget()
        self.center.setObjectName("outer")
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)
        self.mainHLayout = QHBoxLayout()
        self.center.setLayout(self.mainHLayout)

        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.clicked.connect(lambda: self.graphicsView.update_view(1.1))
        self.zoom_out_button = QPushButton("-")
        self.zoom_out_button.clicked.connect(lambda: self.graphicsView.update_view(0.9))
        self.select_button = QPushButton(cm.tr().edit.select_button)
        self.select_button.clicked.connect(lambda: self._select_points())
        self.reset_button = QPushButton(cm.tr().edit.reset_button)
        self.reset_button.clicked.connect(lambda: self.scene.reset_selection_box())
        self.accept_button = QPushButton(cm.tr().edit.accept_button)
        self.accept_button.clicked.connect(lambda: self._accept_selection())
        self.v_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.points = [x[0] for x in dm.get_cutout_points(self.idx)]
        self.scene = MainScene(canvas, self.points, self.accept_button)
        self.graphicsView = EditView(self.scene)

        self.mainHLayout.addWidget(self.graphicsView, 9)
        self.barFrame = QWidget()
        self.mainHLayout.addWidget(self.barFrame, 1)
        self.verticalBar = QVBoxLayout()
        self.verticalBar.setAlignment(Qt.AlignBottom)
        self.barFrame.setLayout(self.verticalBar)

        for i in [self.zoom_in_button, self.zoom_out_button]:
            self.verticalBar.addWidget(i)
        self.verticalBar.addItem(self.v_spacer)
        for i in [self.select_button, self.reset_button, self.accept_button]:
            self.verticalBar.addWidget(i)

        self.sw = sw
        self.sw.addWidget(self)
        self.sw.setCurrentIndex(len(self.sw)-1)

        css = ["edit.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    def _accept_selection(self):
        p = geo.get_corners_from_anchors(*self.scene.selection_box.get_points_from_anchors())
        dm.update_cutout(self.idx, p)
        self.label.update_pixmap()
        self.sw.removeWidget(self)
        self.sw.setCurrentIndex(2)

    def _select_points(self):
        self.accept_button.setEnabled(False)
        self.scene.select_points()
