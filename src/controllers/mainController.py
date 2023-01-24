from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from src import dataManager as Dm
from src.operations import graphicOperations as Go
from src.controllers.editController import EditUi
from src.labelClass import Label


class MainUi(QMainWindow):

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

        self.saveButton = QPushButton("SAVE")
        self.saveButton.clicked.connect(lambda: self.__save_images())
        self.nextButton = QPushButton("NEXT")
        self.nextButton.clicked.connect(lambda: self.load_new_image())
        self.endButton = QPushButton("QUIT")
        self.endButton.clicked.connect(lambda: self.__switch_to_drop())
        for i in [self.saveButton, self.nextButton, self.endButton]:
            i.setMinimumSize(80, 20)
            i.setMaximumSize(160, 40)
            self.buttonHLayout.addWidget(i)

        self.setStyleSheet(open('css/main.css').read())

    def __clear_scroll_area(self):
        # TODO CHECK DELETION
        for i in reversed(range(self.gridLayout.count())):
            a = self.gridLayout.itemAt(i)
            for j in reversed(range(a.layout().count())):
                a.layout().itemAt(j).widget().setParent(None)
            a.layout().setParent(None)

    def load_new_image(self):
        self.__clear_scroll_area()
        Dm.get_new_canvas()
        Dm.generate_cutouts()
        self.nextButton.setEnabled(not Dm.is_empty())
        self.scrollArea.verticalScrollBar().minimum()
        self.fileNameLabel.setText(Dm.get_file_name())
        counter = 0
        for key, co in Dm.get_cutouts().items():
            layout = self.__build_item(self.scrollArea, counter, key, co.img)
            x, y = counter % 2, counter // 2
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

    def __build_item(self, parent, idx, key, img):
        h_layout = QHBoxLayout()
        frame = QFrame()
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        label = Label(parent, img, idx)
        rot_button = self.__build_rotate_button(25, frame, idx, label)
        edi_button = self.__build_edit_button(25, frame, idx, label)
        rem_button = self.__build_remove_button(25, frame, key, label)
        for i in [rot_button, edi_button, rem_button]:
            v_layout.addWidget(i)
        h_layout.addWidget(label, 9)
        h_layout.addWidget(frame, 1)
        return h_layout

    def __build_button(self, size, parent, icon_path):
        button = QPushButton(parent=parent)
        button.setFixedSize(size, size)
        button.setIcon(QIcon(icon_path))
        icon_size = size - 5
        button.setIconSize(QSize(icon_size, icon_size))
        return button

    def __build_remove_button(self, size, parent, key, label):
        button = self.__build_button(size, parent, "assets/rem.png")
        button.setObjectName("rem")
        button.clicked.connect(lambda: self.__toggle_cutout(key, label))
        return button

    def __build_rotate_button(self, size, parent, idx, label):
        button = self.__build_button(size, parent, "assets/rot.png")
        button.setObjectName("rot")
        button.clicked.connect(lambda: self.__rotate_cutout(idx, label))
        return button

    def __build_edit_button(self, size, parent, idx, label):
        button = self.__build_button(size, parent, "assets/edit.png")
        button.setObjectName("edit")
        button.clicked.connect(lambda: self.__open_edit(idx, label))
        return button

    def __open_edit(self, idx, label):
        EditUi(self.sw, idx, label, Dm.get_canvas())

    def __rotate_cutout(self, idx, label):
        Dm.rotate_cutout(idx)
        label.updatePixMap()

    def __toggle_cutout(self, key, label):
        Dm.toggle_cutout(key)
        label.updatePixMap()

    def __save_images(self):
        Dm.save_cutouts()

    def __switch_to_drop(self):
        Dm.clear_data()
        self.__clear_scroll_area()
        self.sw.setCurrentIndex(1)
