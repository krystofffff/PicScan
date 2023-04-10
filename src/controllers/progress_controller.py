from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QHBoxLayout, QFrame
import src.managers.data_manager as dm
import src.managers.config_manager as cm
import src.managers.hash_manager as hm
from PyQt5.QtWidgets import QStackedWidget
from definitions import CSS_DIR
import datetime


class Worker(QObject):
    finished = pyqtSignal()

    def run(self):
        dm.process_next_image()
        self.finished.emit()


class ProgressUi(QMainWindow):
    main_update = pyqtSignal()
    hash_update = pyqtSignal()

    def __init__(self, sw: QStackedWidget):
        super(ProgressUi, self).__init__()
        self.sw = sw
        self.center = QLabel()
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

        css = ["progress.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

    @pyqtSlot(bool)
    def process(self, in_auto_mode):
        self.update_processed()
        self.sw.setCurrentIndex(1)
        if dm.is_empty():
            self.update_processed()
            if cm.get_duplicity_mode() == 1:
                hm.remove_non_similar()
                if hm.is_empty():
                    self.sw.setCurrentIndex(4)
                else:
                    self.hash_update.emit()
                    self.sw.setCurrentIndex(3)
            else:
                self.sw.setCurrentIndex(4)
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
            dm.save_cutouts()
            self.process(in_auto_mode)
        else:
            self.switch_to_main_controller()

    def switch_to_main_controller(self):
        self.main_update.emit()
        self.sw.setCurrentIndex(2)

    def update_processed(self):
        fc = dm.get_file_count()
        fcr = dm.get_file_counter()
        t = dm.get_process_timer()
        fc = 1 if fc == 0 else fc
        if not fcr == 0:
            remaining_t = int((fc - fcr) * (t / fcr))
            self.label_time.setText(f"{cm.tr().progress.label_time} {datetime.timedelta(seconds=remaining_t)}")
        else:
            self.label_time.setText(f"{cm.tr().progress.label_time} ...")
        self.progress_bar.setValue(int(fcr * 1.0 / fc * 100))
        self.label_files.setText(f"{cm.tr().progress.label_files} {fcr}/{fc}")
