import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget

from src.controllers.dropController import DropUi
from src.controllers.mainController import MainUi
import src.managers.configManager as cM


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    cM.load_config()

    sw = QStackedWidget()
    sw.setWindowTitle("PicScan beta")
    main = MainUi(sw)
    drop = DropUi(sw, main)
    for i in [main, drop]:
        sw.addWidget(i)
    sw.setCurrentIndex(1)
    sw.show()
    app.exec_()
