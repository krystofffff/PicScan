from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStackedWidget

import src.managers.config_manager as cm
import src.managers.data_manager as dm
import src.managers.hash_manager as hm
from definitions import ICON_PATH
from src.controllers.popup_dialog import PopupDialog


class StackedWidget(QStackedWidget):
    check_folder = pyqtSignal()

    def __init__(self):
        super(StackedWidget, self).__init__()
        self.setWindowIcon(QIcon(ICON_PATH))

    def closeEvent(self, event) -> None:
        if PopupDialog(cm.tr().stacked.popup_dialog).exec_():
            event.accept()
        else:
            event.ignore()

    def switch_to_drop(self):
        dm.clear_data()
        hm.clear_hashes()
        self.check_folder.emit()
        self.setCurrentIndex(0)
