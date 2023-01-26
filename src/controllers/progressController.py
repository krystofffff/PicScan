import time
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
import src.managers.dataManager as Dm
import src.managers.configManager as Cm
from PyQt5.QtWidgets import QStackedWidget


class Worker(QObject):
    finished = pyqtSignal()

    def run(self):
        Dm.process_next_image()
        self.finished.emit()


class ProgressUi(QMainWindow):
    main_update = pyqtSignal()

    def __init__(self, sw: QStackedWidget):
        super(ProgressUi, self).__init__()
        self.sw = sw
        self.center = QLabel()
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)

        self.label = QLabel()
        self.update_processed()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.setAlignment(Qt.AlignCenter)

        self.center.setLayout(self.layout)

        self.setStyleSheet(open('css/drop.css').read())

    @pyqtSlot(bool)
    def process(self, in_auto_mode):
        if Dm.is_empty():
            self.update_processed()
            self.label.setText(f"FINISHED!\n{self.label.text()}")
        else:
            self.run_thread(in_auto_mode)

    def run_thread(self, in_auto_mode):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(lambda: self.next_step(in_auto_mode))

    def next_step(self, in_auto_mode):
        self.update_processed()
        if in_auto_mode:
            if Cm.get_similarity_mode() == 2 and Dm.any_disabled_cutouts():
                self.switch_to_main_controller()
            else:
                Dm.save_cutouts()
                self.process(in_auto_mode)
        else:
            self.switch_to_main_controller()

    def switch_to_main_controller(self):
        self.main_update.emit()
        self.sw.setCurrentIndex(2)

    def update_processed(self):
        saved = Dm.get_saved_cutouts_counter()
        discarded = Dm.get_discarded_cutouts_counter()
        self.label.setText(f"Saved / Checked: {saved} / {saved + discarded}")
