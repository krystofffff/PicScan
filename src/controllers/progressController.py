import time

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QHBoxLayout, QFrame
import src.managers.dataManager as Dm
import src.managers.configManager as Cm
from PyQt5.QtWidgets import QStackedWidget
from definitions import ROOT_DIR
import datetime


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
        self.center.setObjectName("A")
        self.center.setMinimumSize(960, 480)
        self.setCentralWidget(self.center)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("ProgressBar")
        self.progress_bar.setMaximumSize(500, 50)
        self.progress_bar.setValue(0)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress_bar)
        self.layout.setAlignment(Qt.AlignCenter)

        self.frame = QFrame()
        self.frame.setMaximumSize(500, 50)
        self.label_time = QLabel()
        self.label_files = QLabel()
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.label_time)
        self.h_layout.addStretch()
        self.h_layout.addWidget(self.label_files)
        self.frame.setLayout(self.h_layout)

        self.layout.addWidget(self.frame)

        self.center.setLayout(self.layout)

        self.update_processed()

        self.setStyleSheet(open(ROOT_DIR + '/css/drop.css').read())
        self.setStyleSheet(open(ROOT_DIR + '/css/progress.css').read())

    @pyqtSlot(bool)
    def process(self, in_auto_mode):
        if Dm.is_empty():
            self.update_processed()
            self.label.setText(f"FINISHED!")
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
        # saved = Dm.get_saved_cutouts_counter()
        # discarded = Dm.get_discarded_cutouts_counter()
        fc = Dm.get_file_count()
        fcr = Dm.get_file_counter()
        t = Dm.get_process_timer()
        fc = 1 if fc == 0 else fc
        if not fcr == 0:
            remaining_t = int((fc - fcr) * (t / fcr))
        else:
            remaining_t = 0
        self.progress_bar.setValue(int(fcr * 1.0 / fc * 100))
        self.label_time.setText(f"Time remaining: {datetime.timedelta(seconds=remaining_t)}")
        self.label_files.setText(f"Files processed: {fcr}/{fc}")
        # self.label.setText(f"Saved / Checked: {saved} / {saved + discarded}")
