from PyQt5.QtWidgets import QStackedWidget

from src.controllers.popupDialog import PopupDialog


class StackedWidget(QStackedWidget):

    def closeEvent(self, event) -> None:
        if PopupDialog("Exit ?").exec_():
            event.accept()
        else:
            event.ignore()
