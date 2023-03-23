from PyQt5.QtWidgets import QStackedWidget

from src.controllers.popup_dialog import PopupDialog
import src.managers.config_manager as cm


class StackedWidget(QStackedWidget):

    def closeEvent(self, event) -> None:
        if PopupDialog(cm.tr().stacked.popup_dialog).exec_():
            event.accept()
        else:
            event.ignore()
