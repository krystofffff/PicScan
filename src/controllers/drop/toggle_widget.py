from PyQt5.QtCore import Qt, QPoint, QRectF, pyqtSlot
from PyQt5.QtGui import QPen, QBrush, QColor, QPaintEvent, QPainter, QFont
from PyQt5.QtWidgets import QCheckBox


class ToggleSwitch(QCheckBox):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    _black_pen = QPen(Qt.black)

    def __init__(self, parent=None, bar_color="#B3BBBC", checked_color="#00B0FF", handle_color=Qt.white, fontSize=10):
        super().__init__(parent)

        self._bar_brush = QBrush(QColor(bar_color))
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self.setContentsMargins(0, 0, 0, 0)
        self._handle_position = 0
        self._fontSize = fontSize

        self.stateChanged.connect(self.handle_state_change)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):

        cont_rect = self.contentsRect()
        width = cont_rect.width()
        height = cont_rect.height()
        handle_radius = round(0.25 * height)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        bar_rect = QRectF(0, 0, width - handle_radius, 0.40 * height)
        bar_rect.moveCenter(cont_rect.center())
        rounding = 5

        trail_length = cont_rect.width() - 2 * handle_radius
        x_left = cont_rect.center().x() - (trail_length + handle_radius) / 2
        x_pos = x_left + handle_radius + (trail_length - handle_radius) * self._handle_position
        p.setFont(QFont('Helvetica', self._fontSize, 60))

        text_rect = QRectF(0 + handle_radius, 0, width - 2 * handle_radius, height-2)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(bar_rect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)
            p.setPen(self._black_pen)
            p.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, "AUTO")
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(bar_rect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)
            p.setPen(self._black_pen)
            p.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, "OFF")

        p.setPen(self._transparent_pen if self.isChecked() else self._light_grey_pen)
        p.drawRoundedRect(
            QRectF(x_pos - handle_radius, bar_rect.center().y() - handle_radius, handle_radius * 2, handle_radius * 2),
            rounding, rounding)
        p.end()

    @pyqtSlot(int)
    def handle_state_change(self, value):
        self._handle_position = 1 if value else 0
