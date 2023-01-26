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
        self.mainHLayout = QHBoxLayout()
        self.center.setLayout(self.mainHLayout)
        self.canvas = QLabel()
        self.mainHLayout.addWidget(self.canvas, 5)
        self.VLayout = QVBoxLayout()
        self.mainHLayout.addLayout(self.VLayout, 5)
        self.scrollArea = QScrollArea(widgetResizable=True)
        self.VLayout.addWidget(self.scrollArea, 9)
        self.gridLayout = QGridLayout()
        self.scrollInnerContainer = QWidget()
        self.scrollInnerContainer.setLayout(self.gridLayout)
        self.scrollArea.setWidget(self.scrollInnerContainer)
        self.buttonHLayout = QHBoxLayout()
        self.fileNameLabel = QLabel()
        self.fileNameLabel.setAlignment(Qt.AlignCenter)
        self.VLayout.addWidget(self.fileNameLabel, 1)
        self.VLayout.addLayout(self.buttonHLayout, 1)

        self.save_button = QPushButton("SAVE")
        self.save_button.clicked.connect(lambda: self._save_images())
        self.next_button = QPushButton("NEXT")
        self.next_button.clicked.connect(lambda: self.switch_to_progress(False))
        self.auto_button = QPushButton("AUTO")
        self.auto_button.clicked.connect(lambda: self.switch_to_progress(True))
        self.quit_button = QPushButton("QUIT")
        self.quit_button.clicked.connect(lambda: self._switch_to_drop())
        for i in [self.save_button, self.next_button, self.auto_button, self.quit_button]:
            i.setMinimumSize(80, 20)
            i.setMaximumSize(160, 40)
            self.buttonHLayout.addWidget(i)

        self.setStyleSheet(open('css/main.css').read())

    def _clear_scroll_area(self):
        # TODO CHECK DELETION (QFrame content?)
        for i in reversed(range(self.gridLayout.count())):
            a = self.gridLayout.itemAt(i)
            for j in reversed(range(a.layout().count())):
                a.layout().itemAt(j).widget().setParent(None)
            a.layout().setParent(None)

    def switch_to_progress(self, in_auto_mode):
        # TODO LINK TO AUTO BUTTON
        self.progress.emit(in_auto_mode)
        self.sw.setCurrentIndex(1)

    @pyqtSlot()
    def load_new_image(self):
        self._clear_scroll_area()

        self.next_button.setEnabled(not Dm.is_empty())
        self.scrollArea.verticalScrollBar().minimum()
        self.fileNameLabel.setText(Dm.get_file_name())
        counter = 0
        # TODO COLUMN_COUNT IN SETTINGS ?
        COLUMN_COUNT = 2
        for key, co in Dm.get_cutouts().items():
            layout = self._build_item(self.scrollArea, counter, key, co.img)
            x, y = counter % COLUMN_COUNT, counter // COLUMN_COUNT
            counter += 1
            self.gridLayout.addLayout(layout, y, x)
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

    def _build_item(self, parent, idx, key, img):
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

    def _save_images(self):
        Dm.save_cutouts()

    def _switch_to_drop(self):
        Dm.clear_data()
        self._clear_scroll_area()
        self.sw.setCurrentIndex(0)
