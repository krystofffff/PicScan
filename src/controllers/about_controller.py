from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFrame, QHBoxLayout
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
        self.setFixedSize(500, 500)
        self.setLayout(self.layout)

        self.build_app_name()

        self.build_top()
        self.build_source()
        self.build_version()
        self.layout.addStretch()
        self.build_university()

        css = ["config.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

        self.exec_()

    def build_app_name(self):
        app_name = QLabel("PicScan")
        app_name.setAlignment(Qt.AlignHCenter)
        app_name.setStyleSheet("""font-size: 24px;""")
        self.layout.addWidget(app_name)

    def build_top(self):
        frame_authors = QFrame()

        layout_h = QHBoxLayout()
        layout_authors = QVBoxLayout()

        label_authors_title = QLabel(cm.tr().about.label_authors_title)
        authors = "\n".join(AUTHORS)
        label_authors = QLabel(authors)
        for i in [label_authors_title, label_authors]:
            layout_authors.addWidget(i)

        label_app = QLabel()
        label_app.setAlignment(Qt.AlignCenter)
        img = gra.load_image(f"{ASSETS_PATH}/icon/logo_256x256.png")
        pxmp = gra.get_qpixmap(img)
        label_app.setPixmap(pxmp.scaledToWidth(120, Qt.SmoothTransformation))

        layout_h.addLayout(layout_authors,1)
        layout_h.addWidget(label_app)
        frame_authors.setLayout(layout_h)
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
        frame_university = QFrame()
        layout_v = QVBoxLayout()

        layout_h = QHBoxLayout()
        label_description = QLabel(cm.tr().about.label_description)
        label_description.setWordWrap(True)
        label_kip = QLabel()
        label_kip.setAlignment(Qt.AlignCenter)
        img = gra.load_image(f"{ASSETS_PATH}/kip_logo.jpg")
        pxmp = gra.get_qpixmap(img)
        label_kip.setPixmap(pxmp.scaledToWidth(80, Qt.SmoothTransformation))
        layout_h.addWidget(label_description,1)
        layout_h.addWidget(label_kip)

        label_university = QLabel()
        label_university.setAlignment(Qt.AlignCenter)
        img = gra.load_image(f"{ASSETS_PATH}/university_logo.png")
        pxmp = gra.get_qpixmap(img)
        label_university.setPixmap(pxmp.scaledToWidth(300, Qt.SmoothTransformation))

        layout_v.addLayout(layout_h)
        layout_v.addWidget(label_university)
        frame_university.setLayout(layout_v)

        self.layout.addWidget(frame_university)
