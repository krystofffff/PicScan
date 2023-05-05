from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QHBoxLayout)
from definitions import CSS_DIR, ICON_PATH
import src.managers.config_manager as cm


class FeedbackDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(cm.tr().feedback.window_title)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.setFixedSize(500, 500)
        self.setLayout(self.layout)

        self.build_tutorial_label()

        self.build_tutorial_text()

        self.build_feedback_buttons()

        css = ["config.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

        self.exec_()

    def build_tutorial_label(self):
        tutorial_label = QLabel(cm.tr().feedback.tutorial_title)
        tutorial_label.setAlignment(Qt.AlignHCenter)
        tutorial_label.setStyleSheet("""font-size: 24px;""")
        self.layout.addWidget(tutorial_label)

    def build_tutorial_text(self):
        tutorial_steps = cm.tr().feedback.tutorial_text.split('\n')

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        for step in tutorial_steps:
            if '{github_issues_link}' in step:
                link = "https://github.com/krystofffff/PicScan/issues"
                step = step.format(github_issues_link='<a href="{}">{}</a>'.format(link, link))
                step_label = QLabel(step)
                step_label.setOpenExternalLinks(True)
            else:
                step_label = QLabel(step)

            step_label.setWordWrap(True)
            step_label.setStyleSheet("font-size: 16px;")
            scroll_layout.addWidget(step_label)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)

    def build_feedback_buttons(self):
        close_button = QPushButton(cm.tr().feedback.close_button)
        close_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(close_button)
        self.layout.addLayout(button_layout)
