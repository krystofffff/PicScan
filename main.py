import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget

from src.controllers.dropController import DropUi
from src.controllers.main.mainController import MainUi
from src.controllers.progressController import ProgressUi
import src.managers.configManager as Cm
import src.managers.hashManager as Hm


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    Cm.load_config()
    Hm.load_hashes()

    sw = QStackedWidget()
    sw.setWindowTitle("PicScan beta")
    main = MainUi(sw)
    progress = ProgressUi(sw)
    drop = DropUi(sw)
    main.progress.connect(progress.process)
    drop.progress.connect(progress.process)
    progress.main_update.connect(main.load_new_image)
    for i in [drop, progress, main]:
        sw.addWidget(i)
    sw.setCurrentIndex(0)
    sw.show()

    app.exec_()
