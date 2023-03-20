from PyQt5.QtWidgets import QStackedWidget

from src.controllers.popup_dialog import PopupDialog


class StackedWidget(QStackedWidget):

    def closeEvent(self, event) -> None:
        if PopupDialog("Close this app ?").exec_():
            event.accept()
        else:
            event.ignore()
