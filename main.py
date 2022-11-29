import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStackedWidget

from dropController import DropUi
from mainController import MainUi


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sw = QStackedWidget()
    sw.setWindowTitle("PicScan beta")
    main = MainUi(sw)
    drop = DropUi(sw, main)
    for i in [main, drop]:
        sw.addWidget(i)
    sw.setCurrentIndex(1)
    sw.show()
    app.exec_()
