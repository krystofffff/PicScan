import src.managers.configManager as Cm
from PyQt5.QtWidgets import *


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setStyleSheet(open('css/settings.css').read())

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.setLayout(self.layout)

        self.setMinimumSize(360, 240)

        self._build_output_format_settings()
        self._build_output_folder_settings()
        self.layout.addStretch()
        self._build_save_button()

        self.load_config()

        self.exec_()

    def _build_output_format_settings(self):
        self.frame_o_format = QFrame()
        self.layout_output_format = QVBoxLayout()
        self.frame_o_format.setLayout(self.layout_output_format)
        self.label_format_title = QLabel("Output format:")
        self.label_format_title.setMaximumSize(240, 50)
        self.radio_button_jpg = QRadioButton("JPG")
        self.radio_button_jpg.clicked.connect(lambda: Cm.set_output_format(0))
        self.radio_button_png = QRadioButton("PNG")
        self.radio_button_png.clicked.connect(lambda: Cm.set_output_format(1))
        self.radio_buttons = [self.radio_button_jpg, self.radio_button_png]
        for i in [self.label_format_title, *self.radio_buttons]:
            self.layout_output_format.addWidget(i)
        self.layout.addWidget(self.frame_o_format)

    def _build_save_button(self):
        self.button_save = QPushButton("Save")
        self.button_save.setMinimumSize(80, 40)
        self.button_save.setMaximumSize(160, 40)
        self.button_save.clicked.connect(lambda: Cm.save_config())
        self.layout_buttons = QHBoxLayout()

        self.layout_buttons.addWidget(self.button_save)
        self.layout.addLayout(self.layout_buttons)

    def load_config(self):
        Cm.create_temp_config()
        self.radio_buttons[Cm.get_output_format()].toggle()
        self.label_o_folder.setText(Cm.get_output_folder())

    def _build_output_folder_settings(self):
        self.frame_o_folder = QFrame()
        self.layout_o_folder_outer = QVBoxLayout()
        self.frame_o_folder.setLayout(self.layout_o_folder_outer)
        self.label_o_folder_title = QLabel("Output folder:")
        self.layout_o_folder = QHBoxLayout()
        self.label_o_folder = QLabel(Cm.get_output_folder())
        self.button_browse_o_folder = QPushButton("Browse")
        self.button_browse_o_folder.clicked.connect(lambda: self.browse_output_folder())
        self.button_browse_o_folder.setMinimumSize(60, 30)
        self.button_browse_o_folder.setMaximumSize(80, 40)
        self.button_browse_o_folder.setObjectName("browse")
        for i in [self.label_o_folder, self.button_browse_o_folder]:
            self.layout_o_folder.addWidget(i)
        self.layout_o_folder.addStretch()
        self.layout_o_folder_outer.addWidget(self.label_o_folder_title)
        self.layout_o_folder_outer.addLayout(self.layout_o_folder)
        self.layout.addWidget(self.frame_o_folder)

    def browse_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select folder')
        if folder == "":
            return
        Cm.set_output_folder(folder)
        self.label_o_folder.setText(folder)
