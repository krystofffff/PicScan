import statistics as stat

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem

import geometricOperations as Geo


def _get_point_from_anchor(anchor):
    return [anchor.scenePos().x(), anchor.scenePos().y()]


class Anchor(QGraphicsEllipseItem):

    def __init__(self, point, r, rect, color):
        super().__init__(0, 0, r, r)
        self.r = r
        self.setPos(point[0] - r//2, point[1] - r//2)
        pen = QPen()
        pen.setWidth(25)
        pen.setColor(color)
        self.setPen(pen)
        self.setAcceptHoverEvents(True)
        self.rect = rect

    def mousePressEvent(self, event):
        pass

    def get_point(self):
        return [self.pos().x() + self.r//2, self.pos().y() + self.r//2]


class CornerAnchor(Anchor):

    def mouseMoveEvent(self, event):
        orig_cursor = event.lastScenePos()
        updated_cursor = event.scenePos()
        orig_anchor = self.scenePos()
        diff_cursor_x = updated_cursor.x() - orig_cursor.x()
        diff_cursor_y = updated_cursor.y() - orig_cursor.y()
        self.setPos(diff_cursor_x + orig_anchor.x(), diff_cursor_y + orig_anchor.y())
        self.rect.update_lines()


class SlideAnchor(Anchor):

    def __init__(self, *args, a1, a2):
        super().__init__(*args)
        self.a1 = a1
        self.a2 = a2

    def mouseMoveEvent(self, event):
        orig_cursor = event.lastScenePos()
        updated_cursor = event.scenePos()
        orig_anchor = self.scenePos()
        diff_cursor_x = updated_cursor.x() - orig_cursor.x()
        diff_cursor_y = updated_cursor.y() - orig_cursor.y()
        self.setPos(diff_cursor_x + orig_anchor.x(), diff_cursor_y + orig_anchor.y())
        # p1 = _get_point_from_anchor(self.a1)
        # p2 = _get_point_from_anchor(self.a2)
        # angle1 = Geo.get_angle(p1, p2) - math.pi/2
        # angle2 = Geo.get_angle([orig_cursor.x(), orig_cursor.y()], [updated_cursor.x(), updated_cursor.y()])
        # angle_fin = angle2 - angle1
        # length = math.sqrt(diff_cursor_x**2 + diff_cursor_y**2)
        # a = math.cos(angle_fin) * length
        # self.setPos(math.cos(angle1) * a + orig_anchor.x(), math.sin(angle1) * a + orig_anchor.y())
        self.rect.update_lines()


class Line(QGraphicsLineItem):

    def __init__(self, a_radius, width):
        super().__init__(0, 0, 0, 0)
        self.a_size = a_radius
        self.setPen(QtGui.QPen(QtGui.QColor(50, 50, 50), width, QtCore.Qt.DashLine))

    def update_pos(self, p1, p2):
        self.setLine(p1[0], p1[1], p2[0], p2[1])


class SelectionBox:

    def __init__(self, scene, points):
        self.points = points
        self.scene = scene
        self.a_radius = 100
        self.lines = [Line(self.a_radius, 10) for _ in range(4)]
        point_mid = [stat.mean([self.points[2][0], self.points[3][0]]),
                     stat.mean([self.points[2][1], self.points[3][1]])]
        self.anchor1 = CornerAnchor(self.points[0], self.a_radius, self, Qt.red)
        self.anchor2 = CornerAnchor(self.points[1], self.a_radius, self, Qt.red)
        self.anchor3 = SlideAnchor(point_mid, self.a_radius, self, Qt.blue, a1=self.anchor1, a2=self.anchor2)
        self.update_lines()
        for i in self.lines:
            self.scene.addItem(i)
        for i in [self.anchor1, self.anchor2, self.anchor3]:
            self.scene.addItem(i)

    def drop_all(self):
        self.scene.removeItem(self.anchor1)
        self.scene.removeItem(self.anchor2)
        self.scene.removeItem(self.anchor3)
        for i in self.lines:
            self.scene.removeItem(i)

    def get_points_from_anchors(self):
        return self.anchor1.get_point(), \
               self.anchor2.get_point(), \
               self.anchor3.get_point()

    def update_lines(self):
        points = Geo.get_corners_from_anchors(*self.get_points_from_anchors())
        for idx, line in enumerate(self.lines):
            line.update_pos(points[idx % 4], points[(idx + 1) % 4])
