from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStackedWidget

import src.managers.config_manager as cm
from definitions import ICON_PATH
from src.controllers.popup_dialog import PopupDialog


class StackedWidget(QStackedWidget):

    def __init__(self):
        super(StackedWidget, self).__init__()
        self.setWindowIcon(QIcon(ICON_PATH))

    def closeEvent(self, event) -> None:
        if PopupDialog(cm.tr().stacked.popup_dialog).exec_():
            event.accept()
        else:
            event.ignore()
