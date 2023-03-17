from PyQt5.QtCore import Qt, QPoint, QRectF, pyqtSlot, pyqtProperty
from PyQt5.QtGui import QPen, QBrush, QColor, QPaintEvent, QPainter, QFont
from PyQt5.QtWidgets import QCheckBox


class ToggleSwitch(QCheckBox):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    _black_pen = QPen(Qt.black)

    def __init__(self,
                 parent=None,
                 bar_color="#B3BBBC",
                 checked_color="#00B0FF",
                 handle_color=Qt.white,
                 h_scale=1.0,
                 v_scale=1.0,
                 fontSize=10):

        super().__init__(parent)

        self._bar_brush = QBrush(QColor(bar_color))
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self.setContentsMargins(0, 0, 0, 0)
        self._handle_position = 0
        self._h_scale = h_scale
        self._v_scale = v_scale
        self._fontSize = fontSize

        self.stateChanged.connect(self.handle_state_change)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        width = contRect.width() * self._h_scale
        height = contRect.height() * self._v_scale
        handleRadius = round(0.25 * height)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(0, 0, width - handleRadius, 0.40 * height)
        barRect.moveCenter(contRect.center())
        rounding = 5

        trailLength = contRect.width() * self._h_scale - 2 * handleRadius
        xLeft = contRect.center().x() - (trailLength + handleRadius) / 2
        xPos = xLeft + handleRadius + (trailLength - handleRadius) * self._handle_position
        p.setFont(QFont('Helvetica', self._fontSize, 60))

        textRect = QRectF(0 + handleRadius, 0, width - 2 * handleRadius, height-2)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)
            p.setPen(self._black_pen)
            p.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, "AUTO")
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)
            p.setPen(self._black_pen)
            p.drawText(textRect, Qt.AlignRight | Qt.AlignVCenter, "OFF")

        p.setPen(self._transparent_pen if self.isChecked() else self._light_grey_pen)
        p.drawRoundedRect(
            QRectF(xPos - handleRadius, barRect.center().y() - handleRadius, handleRadius * 2, handleRadius * 2),
            rounding, rounding)
        p.end()

    @pyqtSlot(int)
    def handle_state_change(self, value):
        self._handle_position = 1 if value else 0

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    def setH_scale(self, value):
        self._h_scale = value
        self.update()

    def setV_scale(self, value):
        self._v_scale = value
        self.update()

    def setFontSize(self, value):
        self._fontSize = value
        self.update()
