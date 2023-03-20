import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from src.controllers.drop.dropController import DropUi
from src.controllers.endController import EndUI
from src.controllers.main.mainController import MainUi
from src.controllers.progressController import ProgressUi
from src.controllers.sim.simController import SimUI
from src.controllers.stackedWidget import StackedWidget
import src.managers.configManager as Cm
import src.managers.nnRotManager as Nm

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

    main = MainUi(sw)
    progress = ProgressUi(sw)
    sim = SimUI(sw)
    end = EndUI(sw)

    main.progress.connect(progress.process)
    drop.progress.connect(progress.process)
    progress.main_update.connect(main.load_new_image)
    progress.hash_update.connect(sim.load_new_image)

    for i in [drop, progress, main, sim, end]:
        sw.addWidget(i)
    sw.setCurrentIndex(0)
    sw.show()

    app.exec_()
