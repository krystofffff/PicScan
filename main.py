from PyQt5 import QtWidgets
import sys
import dataManager as Dm

from dropController import DropUi
from mainController import MainUi

if __name__ == "__main__":
    dm = Dm.DataManager()
    app = QtWidgets.QApplication(sys.argv)
    sw = QtWidgets.QStackedWidget()
    main = MainUi(sw, dm)
    drop = DropUi(sw, dm, main)
    sw.addWidget(main)
    sw.addWidget(drop)
    sw.setCurrentIndex(1)
    sw.show()
    app.exec_()
