from PyQt5.QtCore import pyqtSignal

import src.managers.configManager as Cm
import src.managers.hashManager as Hm
import src.managers.nnRotManager as Nm
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFrame, QLabel, QRadioButton, QPushButton, QHBoxLayout, QFileDialog, \
    QCheckBox
from definitions import ROOT_DIR, CSS_DIR


class ConfigDialog(QDialog):
    start_loading = pyqtSignal(bool)

    def __init__(self, drop):
        super().__init__()
        self.setWindowTitle("Settings")

        self.start_loading.connect(drop.stop_nn_loading)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.setLayout(self.layout)

        self.setMinimumSize(640, 480)

        self._build_output_format_settings()
        self._build_output_folder_settings()
        self._build_similar_settings()

        self._build_nn_loading_settings()

        self.layout.addStretch()
        self._build_save_button()

        self.load_config()

        css = ["config.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

        self.exec_()

    def _build_nn_loading_settings(self):
        self.frame_nn_loading = QFrame()
        self.layout_nn_loading = QVBoxLayout()
        self.frame_nn_loading.setLayout(self.layout_nn_loading)
        self.label_nn_title = QLabel("Fix rotation using AI:")
        self.checkbox_nn_loading = QCheckBox("Enabled")
        self.checkbox_nn_loading.setChecked(Cm.get_nn_loading())
        self.checkbox_nn_loading.clicked.connect(lambda: Cm.set_nn_loading(self.checkbox_nn_loading.isChecked()))
        self.layout_nn_loading.addWidget(self.label_nn_title)
        self.layout_nn_loading.addWidget(self.checkbox_nn_loading)
        self.layout.addWidget(self.frame_nn_loading)

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
        self.format_radio_buttons = [self.radio_button_jpg, self.radio_button_png]
        for i in [self.label_format_title, *self.format_radio_buttons]:
            self.layout_output_format.addWidget(i)
        self.layout.addWidget(self.frame_o_format)

    def _build_save_button(self):
        self.button_save = QPushButton("Save")
        self.button_save.setMinimumSize(80, 40)
        self.button_save.setMaximumSize(160, 40)
        self.button_save.clicked.connect(lambda: self._save_and_close())
        self.layout_buttons = QHBoxLayout()

        self.layout_buttons.addWidget(self.button_save)
        self.layout.addLayout(self.layout_buttons)

    def _save_and_close(self):
        Cm.save_config()
        if Cm.get_nn_loading() and not Nm.is_model_loaded():
            Nm.load_model_async()
            self.start_loading.emit(False)
        self.close()

    def load_config(self):
        Cm.create_temp_config()
        self.format_radio_buttons[Cm.get_output_format()].toggle()
        self.label_o_folder.setText(Cm.get_output_folder())
        self.s_radio_buttons[Cm.get_similarity_mode()].toggle()

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
        self.button_browse_o_folder.setObjectName("smaller")
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

    def _build_similar_settings(self):
        self.frame_s = QFrame()
        self.layout_s_outer = QHBoxLayout()
        self.frame_s.setLayout(self.layout_s_outer)

        self.layout_s_radios = QVBoxLayout()
        self.label_s = QLabel("Similarity check mode:")
        self.radio_button_s_disable = QRadioButton("Disabled")
        self.radio_button_s_disable.clicked.connect(lambda: Cm.set_similarity_mode(0))
        self.radio_button_s_skip = QRadioButton("Skip similar in AUTO")
        self.radio_button_s_skip.clicked.connect(lambda: Cm.set_similarity_mode(1))
        self.radio_button_s_stop = QRadioButton("Stop on similar in AUTO")
        self.radio_button_s_stop.clicked.connect(lambda: Cm.set_similarity_mode(2))
        self.s_radio_buttons = [self.radio_button_s_disable, self.radio_button_s_skip, self.radio_button_s_stop]
        for i in [self.label_s, *self.s_radio_buttons]:
            self.layout_s_radios.addWidget(i)

        self.layout_hash_records = QHBoxLayout()
        self.label_s_count = QLabel(f"Records: {Hm.get_hash_count()//4}")
        self.button_s_clear_records = QPushButton("Clear records")
        self.button_s_clear_records.setObjectName("smaller")
        self.button_s_clear_records.clicked.connect(lambda: self.clear_hashes())
        for i in [self.label_s_count, self.button_s_clear_records]:
            self.layout_hash_records.addWidget(i)

        self.layout_s_outer.addLayout(self.layout_s_radios)
        self.layout_s_outer.addStretch()
        self.layout_s_outer.addLayout(self.layout_hash_records)

        self.layout.addWidget(self.frame_s)

    def clear_hashes(self):
        Hm.clear_hashes()
        self.label_s_count.setText(f"Records: {Hm.get_hash_count()//4}")
