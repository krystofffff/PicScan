import src.configManager as cM
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
        self.layout.addStretch()
        self._build_save_button()

        self.load_config()

        self.exec_()

    def _build_output_format_settings(self):
        self.layout_output_format = QVBoxLayout()
        self.label_format = QLabel("Output format:")
        self.label_format.setMaximumSize(240, 50)
        self.rad_button_jpg = QRadioButton("JPG")
        self.rad_button_jpg.clicked.connect(lambda: self._output_format_changed(0))
        self.rad_button_png = QRadioButton("PNG")
        self.rad_button_png.clicked.connect(lambda: self._output_format_changed(1))
        self.radio_buttons = [self.rad_button_jpg, self.rad_button_png]
        for i in [self.label_format, *self.radio_buttons]:
            self.layout_output_format.addWidget(i)
        self.layout.addLayout(self.layout_output_format)

    def _build_save_button(self):
        self.save_button = QPushButton("Save")
        self.save_button.setMinimumSize(80, 20)
        self.save_button.setMaximumSize(160, 40)
        self.save_button.clicked.connect(lambda: cM.save_config())
        self.layout_save_button = QHBoxLayout()

        self.layout_save_button.addWidget(self.save_button)
        self.layout.addLayout(self.layout_save_button)

    def _output_format_changed(self, id):
        cM.set_output_format(id)

    def load_config(self):
        cM.create_temp_config()
        self.radio_buttons[cM.get_output_format()].toggle()
