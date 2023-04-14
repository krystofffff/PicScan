from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPlainTextEdit,
                             QHBoxLayout, QPushButton, QMessageBox)
from definitions import CSS_DIR, ICON_PATH


class FeedbackDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Feedback")
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
        feedback_label = QLabel("Feedback")
        feedback_label.setAlignment(Qt.AlignHCenter)
        feedback_label.setStyleSheet("""font-size: 24px;""")
        self.layout.addWidget(feedback_label)

    def build_feedback_input(self):
        self.feedback_input = QPlainTextEdit()
        self.feedback_input.setPlaceholderText("Enter your feedback here...")
        self.layout.addWidget(self.feedback_input)

    def build_feedback_buttons(self):
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_feedback)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)
        self.layout.addLayout(button_layout)

    def submit_feedback(self):
        feedback = self.feedback_input.toPlainText()

        if feedback:
            # TODO: Add logic to send feedback to the desired service
            QMessageBox.information(self, "Success",
                                    "Thank you for your feedback!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error",
                                "Please enter your feedback before submitting.")
