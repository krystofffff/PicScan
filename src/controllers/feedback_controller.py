import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPlainTextEdit,
                             QHBoxLayout, QPushButton, QMessageBox)
from requests.auth import HTTPBasicAuth

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

        self.build_feedback_label()

        self.build_feedback_input()
        self.build_feedback_buttons()

        css = ["config.css", "buttons.css"]
        t = [open(CSS_DIR + x).read() for x in css]
        self.setStyleSheet("".join(t))

        self.exec_()

    def build_feedback_label(self):
        feedback_label = QLabel(cm.tr().feedback.feedback_label)
        feedback_label.setAlignment(Qt.AlignHCenter)
        feedback_label.setStyleSheet("""font-size: 24px;""")
        self.layout.addWidget(feedback_label)

    def build_feedback_input(self):
        self.feedback_input = QPlainTextEdit()
        self.feedback_input.setPlaceholderText(cm.tr().feedback.feedback_input)
        self.layout.addWidget(self.feedback_input)

    def build_feedback_buttons(self):
        submit_button = QPushButton(cm.tr().feedback.submit_button)
        submit_button.clicked.connect(self.submit_feedback)
        cancel_button = QPushButton(cm.tr().feedback.cancel_button)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)
        self.layout.addLayout(button_layout)

    def submit_feedback(self):
        feedback = self.feedback_input.toPlainText()

        if feedback:
            username = 'p22156@student.osu.cz'
            api_token = 'ATATT3xFfGF04RdbgUzoeTlPexCgkYT-zkA-YP-dwxe-S2_dnX_ndkxYqioHwFt4a4A7bxum7rCh99gYvgfW4zmx11GghF55vtTzefNZxDhBrLE03V7Zpq29stSBjFgkBXSq6VKniUjTu1VqdwdUSq_7hFGrVOGgdnfv7MK0hoZ9jOHKkuVGL7w=2CF30DBF'

            project_key = 'PS'
            issue_type = 'Bug'

            issue_data = {
                "fields": {
                    "project": {
                        "key": project_key
                    },
                    "summary": f"Feedback from PicScan: {feedback[:50]}...",
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": feedback
                                    }
                                ]
                            }
                        ]
                    },
                    "issuetype": {
                        "name": issue_type
                    },

                }
            }

            jira_url = 'https://osukip.atlassian.net/rest/api/3/issue'

            response = requests.post(
                jira_url,
                json=issue_data,
                auth=HTTPBasicAuth(username, api_token)
            )

            if response.status_code == 201:
                QMessageBox.information(self, cm.tr().feedback.messageBox_Success,
                                        cm.tr().feedback.messageBox_Thanks)
                self.accept()
            else:
                QMessageBox.warning(self, cm.tr().feedback.messageBox_Error,
                                    f"{cm.tr().feedback.messageBox_Failed}, {response.content}")
        else:
            QMessageBox.warning(self, cm.tr().feedback.messageBox_Error,
                                cm.tr().feedback.messageBox_Please)
