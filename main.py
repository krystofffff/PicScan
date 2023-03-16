import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from src.controllers.dropController import DropUi
from src.controllers.main.mainController import MainUi
from src.controllers.progressController import ProgressUi
import src.managers.configManager as Cm
import src.managers.hashManager as Hm
import src.managers.nnRotManager as Nm
from src.controllers.sim.simController import SimUI
from src.controllers.stackedWidget import StackedWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    Cm.load_config()

    sw = StackedWidget()
    sw.setWindowTitle("PicScan beta")
    drop = DropUi(sw)

    nn_loader = Nm.loader
    nn_loader.is_loaded.connect(drop.stop_nn_loading)
    if Cm.get_nn_loading():
        Nm.load_model_async()

    Hm.load_hashes()

    main = MainUi(sw)
    progress = ProgressUi(sw)
    main.progress.connect(progress.process)
    drop.progress.connect(progress.process)

    # sim = SimUI(sw)
    # sw.addWidget(sim)

    progress.main_update.connect(main.load_new_image)
    for i in [drop, progress, main]:
        sw.addWidget(i)
    sw.setCurrentIndex(0)
    sw.show()

    app.exec_()
