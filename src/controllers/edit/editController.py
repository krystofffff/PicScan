from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, \
    QMainWindow, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy

import src.managers.dataManager as Dm
from src.controllers.edit.editScene import MainScene
from src.controllers.edit.editView import EditView
from src.utils import geometricUtils as Geo


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
        self.select_button = QPushButton("Select\npoints")
        self.select_button.clicked.connect(lambda: self._select_points())
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(lambda: self.scene.reset_selection_box())
        self.accept_button = QPushButton("Ok")
        self.accept_button.clicked.connect(lambda: self._accept_selection())
        self.v_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.points = [x[0] for x in Dm.get_cutout_points(self.idx)]
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
        self.sw.setCurrentIndex(3)

        self.setStyleSheet(open('css/edit.css').read())

    def _accept_selection(self):
        p = Geo.get_corners_from_anchors(*self.scene.selection_box.get_points_from_anchors())
        Dm.update_cutout(self.idx, p)
        self.label.update_pixmap()
        self.sw.removeWidget(self)
        self.sw.setCurrentIndex(2)

    def _select_points(self):
        self.accept_button.setEnabled(False)
        self.scene.select_points()
