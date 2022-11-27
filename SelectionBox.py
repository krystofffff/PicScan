import math
import statistics as stat

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem


class Anchor(QGraphicsEllipseItem):

    def __init__(self, point, r, rect, color):
        super().__init__(0, 0, r, r)
        self.setPos(point[0], point[1])
        pen = QPen()
        pen.setWidth(25)
        pen.setColor(color)
        self.setPen(pen)
        self.setAcceptHoverEvents(True)
        self.rect = rect

    def mousePressEvent(self, event):
        pass


class CornerAnchor(Anchor):

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
        orig_position = self.scenePos()
        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(updated_cursor_x, updated_cursor_y)
        self.rect.update_lines()


class SlideAnchor(Anchor):

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
        orig_position = self.scenePos()
        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(updated_cursor_x, updated_cursor_y)
        self.rect.update_lines()


class Line(QGraphicsLineItem):

    def __init__(self, a_radius, width):
        super().__init__(0, 0, 0, 0)
        self.a_size = a_radius
        self.setPen(QtGui.QPen(QtGui.QColor(150, 150, 150), width, QtCore.Qt.DashLine))

    def update_pos(self, p1, p2):
        self.setLine(p1[0] + self.a_size//2, p1[1] + self.a_size//2, p2[0] + self.a_size//2, p2[1]+ self.a_size//2)


class SelectionBox:

    def __init__(self, scene):
        points = [[500, 500],
                  [100, 500],
                  [100, 100],
                  [500, 100]]
        self.scene = scene
        self.a_radius = 100
        self.lines = [Line(self.a_radius, 10) for _ in range(4)]
        self.points = points
        point_mid = [stat.mean([self.points[2][0], self.points[3][0]]),
                     stat.mean([self.points[2][1], self.points[3][1]])]
        self.anchor1 = CornerAnchor(self.points[0], self.a_radius, self, Qt.red)
        self.anchor2 = CornerAnchor(self.points[1], self.a_radius, self, Qt.red)
        self.anchor3 = SlideAnchor(point_mid, self.a_radius, self, Qt.blue)
        self.update_lines()
        for i in self.lines:
            self.scene.addItem(i)
        for i in [self.anchor1, self.anchor2, self.anchor3]:
            self.scene.addItem(i)

    def _get_points(self):
        p1 = [self.anchor1.scenePos().x(), self.anchor1.scenePos().y()]
        p2 = [self.anchor2.scenePos().x(), self.anchor2.scenePos().y()]
        v1 = p1[0] - p2[0]
        v2 = p1[1] - p2[1]
        d1 = self._get_distance()
        d2 = math.sqrt(v1 ** 2 + v2 ** 2)
        ratio = d1 / d2
        p3 = [p2[0] + v2 * ratio, p2[1] - v1 * ratio]
        p4 = [p1[0] + v2 * ratio, p1[1] - v1 * ratio]
        return [p1, p2, p3, p4]

    def _get_distance(self):
        x0 = self.anchor3.scenePos().x()
        y0 = self.anchor3.scenePos().y()
        x1 = self.anchor1.scenePos().x()
        y1 = self.anchor1.scenePos().y()
        x2 = self.anchor2.scenePos().x()
        y2 = self.anchor2.scenePos().y()
        top = -(x2 - x1) * (y1 - y0) + (x1 - x0) * (y2 - y1)
        bot = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
        return top / bot

    def update_lines(self):
        points = self._get_points()
        for idx, line in enumerate(self.lines):
            line.update_pos(points[idx % 4], points[(idx + 1) % 4])
