import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

import src.managers.config_manager as cm
import src.managers.nn_rot_manager as nm
from src.controllers.drop.drop_controller import DropUi
from src.controllers.end_controller import EndUI
from src.controllers.main.main_controller import MainUi
from src.controllers.progress_controller import ProgressUi
from src.controllers.sim.sim_controller import SimUI
from src.controllers.stacked_widget import StackedWidget
from definitions import APP_VERSION

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    cm.load_config()

    sw = StackedWidget()

    sw.setWindowTitle(f"PicScan {APP_VERSION}")
    drop = DropUi(sw)

    nn_loader = nm.loader
    nn_loader.is_loaded.connect(drop.stop_nn_loading)
    if cm.get_nn_loading():
        nm.load_model_async()

    main = MainUi(sw)
    progress = ProgressUi(sw)
    sim = SimUI(sw)
    end = EndUI(sw)

    main.progress.connect(progress.process)
    drop.progress.connect(progress.process)
    sw.check_folder.connect(drop.update_output_folder_message)
    progress.main_update.connect(main.load_new_image)
    progress.hash_update.connect(sim.load_new_image)

    for i in [drop, progress, main, sim, end]:
        sw.addWidget(i)
    sw.setCurrentIndex(0)
    sw.show()

    app.exec_()
