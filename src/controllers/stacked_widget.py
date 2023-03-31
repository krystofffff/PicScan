import os
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.uic.properties import QtGui

from definitions import ASSETS_PATH
from src.controllers.popup_dialog import PopupDialog
import src.managers.config_manager as cm


class StackedWidget(QStackedWidget):

    def __init__(self):
        super(StackedWidget, self).__init__()
        self.setWindowIcon(QIcon(f"{ASSETS_PATH}/logo/logo_24x24.png"))

    def closeEvent(self, event) -> None:
        if PopupDialog(cm.tr().stacked.popup_dialog).exec_():
            event.accept()
        else:
            event.ignore()
