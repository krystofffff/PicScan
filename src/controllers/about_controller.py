from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFrame
import src.managers.config_manager as cm
import src.utils.graphic_utils as gra
from definitions import CSS_DIR, ICON_PATH, ASSETS_PATH, WEB_URL, APP_VERSION, AUTHORS


class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(cm.tr().about.window_title)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.setFixedSize(320, 400)
        self.setLayout(self.layout)

        self.build_authors()
        self.build_source()
        self.build_version()
        self.layout.addStretch()
        self.build_university()

        css = ["config.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

        self.exec_()

    def build_authors(self):
        frame_authors = QFrame()
        layout_authors = QVBoxLayout()
        frame_authors.setLayout(layout_authors)
        label_authors_title = QLabel(cm.tr().about.label_authors_title)
        authors = "\n".join(AUTHORS)
        label_authors = QLabel(authors)
        for i in [label_authors_title, label_authors]:
            layout_authors.addWidget(i)
        self.layout.addWidget(frame_authors)

    def build_source(self):
        frame_link = QFrame()
        label_link = QLabel()
        label_link.linkActivated.connect(lambda x: QDesktopServices.openUrl(QUrl(WEB_URL)))
        label_link.setText(f"<a href={WEB_URL}>{cm.tr().about.label_link}</a>")
        layout_link = QVBoxLayout()
        layout_link.addWidget(label_link)
        frame_link.setLayout(layout_link)
        self.layout.addWidget(frame_link)

    def build_version(self):
        frame_version = QFrame()
        label_version = QLabel(f"{cm.tr().about.label_version} {APP_VERSION}")
        layout_version = QVBoxLayout()
        layout_version.addWidget(label_version)
        frame_version.setLayout(layout_version)
        self.layout.addWidget(frame_version)

    def build_university(self):
        label_university = QLabel()
        label_university.setAlignment(Qt.AlignCenter)
        img = gra.load_image(f"{ASSETS_PATH}/university.png")
        pxmp = gra.get_qpixmap(img)
        label_university.setPixmap(pxmp.scaledToWidth(250, Qt.SmoothTransformation))
        self.layout.addWidget(label_university)
