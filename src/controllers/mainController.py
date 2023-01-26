from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from src.managers import dataManager as Dm
from src.operations import graphicOperations as Go
from src.controllers.editController import EditUi
from src.labelClass import Label


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

        self.setStyleSheet(open('css/main.css').read())

    def _clear_scroll_area(self):
        # TODO CHECK DELETION (QFrame content?)
        for i in reversed(range(self.grid_layout.count())):
            a = self.grid_layout.itemAt(i)
            for j in reversed(range(a.layout().count())):
                a.layout().itemAt(j).widget().setParent(None)
            a.layout().setParent(None)

    def switch_to_progress(self, in_auto_mode):
        Dm.save_cutouts()
        self.progress.emit(in_auto_mode)
        self.sw.setCurrentIndex(1)

    @pyqtSlot()
    def load_new_image(self):
        self._clear_scroll_area()

        self.scroll_area.verticalScrollBar().minimum()
        self.file_name_label.setText(Dm.get_file_name())
        counter = 0
        # TODO COLUMN_COUNT IN SETTINGS ?
        COLUMN_COUNT = 2
        for key, co in Dm.get_cutouts().items():
            layout = self._build_item(self.scroll_area, counter, key)
            x, y = counter % COLUMN_COUNT, counter // COLUMN_COUNT
            counter += 1
            self.grid_layout.addLayout(layout, y, x)
        self.pixmap = Go.get_qpixmap(Dm.get_canvas())
        self.canvas.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.canvas.setAlignment(Qt.AlignCenter)
        self.update_label()

    def resizeEvent(self, event):
        scaled_size = self.canvas.size()
        scaled_size.scale(self.canvas.size(), Qt.KeepAspectRatio)
        if not self.canvas.pixmap() or scaled_size != self.canvas.pixmap().size():
            self.update_label()

    def update_label(self):
        self.canvas.setPixmap(self.pixmap.scaled(self.canvas.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _build_item(self, parent, idx, key):
        h_layout = QHBoxLayout()
        frame = QFrame()
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        label = Label(parent, idx)
        rot_button = self._build_rotate_button(25, frame, idx, label)
        edi_button = self._build_edit_button(25, frame, idx, label)
        rem_button = self._build_remove_button(25, frame, key, label)
        for i in [rot_button, edi_button, rem_button]:
            v_layout.addWidget(i)
        h_layout.addWidget(label, 9)
        h_layout.addWidget(frame, 1)
        return h_layout

    def _build_button(self, size, parent, icon_path):
        button = QPushButton(parent=parent)
        button.setFixedSize(size, size)
        button.setIcon(QIcon(icon_path))
        icon_size = size - 5
        button.setIconSize(QSize(icon_size, icon_size))
        return button

    def _build_remove_button(self, size, parent, key, label):
        button = self._build_button(size, parent, "assets/rem.png")
        button.setObjectName("rem")
        button.clicked.connect(lambda: self._toggle_cutout(key, label))
        return button

    def _build_rotate_button(self, size, parent, idx, label):
        button = self._build_button(size, parent, "assets/rot.png")
        button.setObjectName("rot")
        button.clicked.connect(lambda: self._rotate_cutout(idx, label))
        return button

    def _build_edit_button(self, size, parent, idx, label):
        button = self._build_button(size, parent, "assets/edit.png")
        button.setObjectName("edit")
        button.clicked.connect(lambda: self._open_edit(idx, label))
        return button

    def _open_edit(self, idx, label):
        # TODO should be persistent ? (+ sw indexing ?)
        EditUi(self.sw, idx, label, Dm.get_canvas())

    def _rotate_cutout(self, idx, label):
        Dm.rotate_cutout(idx)
        label.updatePixMap()

    def _toggle_cutout(self, key, label):
        Dm.toggle_cutout(key)
        label.updatePixMap()

    def _switch_to_drop(self):
        Dm.clear_data()
        self._clear_scroll_area()
        self.sw.setCurrentIndex(0)
