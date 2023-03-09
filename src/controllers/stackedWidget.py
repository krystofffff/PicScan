from PyQt5.QtWidgets import QStackedWidget, QMessageBox


class StackedWidget(QStackedWidget):

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the app ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
