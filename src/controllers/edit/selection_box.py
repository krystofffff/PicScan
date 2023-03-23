import math
import statistics as stat

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QCursor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem

from src.utils import geometric_utils as geo


def qpoint_to_point(p):
    return [p.x(), p.y()]


class Anchor(QGraphicsEllipseItem):

    def __init__(self, point, r, rect, color):
        super().__init__(0, 0, r, r)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.r = r
        self.setPos(self._off_pos(point[0]), self._off_pos(point[1]))
        pen = QPen()
        pen.setWidth(10)
        pen.setColor(color)
        self.setPen(pen)
        self.setAcceptHoverEvents(True)
        self.rect = rect
        self.center_point = QGraphicsEllipseItem(self.r // 2, self.r // 2, 2, 2, self)
        pen = QPen()
        pen.setWidth(0)
        self.center_point.setPen(pen)

    def mousePressEvent(self, event):
        pass

    def get_point(self):
        return [self.pos().x() + self.r // 2, self.pos().y() + self.r // 2]

    def _off_pos(self, i):
        return i - self.r // 2

    def _get_event_points(self, event):
        orig_anchor = self.scenePos()
        orig_cursor = event.lastScenePos()
        updated_cursor = event.scenePos()
        p_oa = qpoint_to_point(orig_anchor)
        p_oc = qpoint_to_point(orig_cursor)
        p_uc = qpoint_to_point(updated_cursor)
        return p_oa, p_oc, p_uc


class CornerAnchor(Anchor):

    def __init__(self, *args):
        super().__init__(*args)
        self.anchor_s = None

    def add_slide_anchor(self, a):
        self.anchor_s = a

    def mouseMoveEvent(self, event):
        p_oa, p_oc, p_uc = self._get_event_points(event)
        v = geo.get_vector_between_points(p_oc, p_uc)
        p = geo.get_point_moved_by_vector(p_oa, v)
        self.setPos(p[0], p[1])
        self.center_point.setPos(0, 0)
        self.anchor_s.corner_moved()
        self.rect.update_lines()


class SlideAnchor(Anchor):

    def __init__(self, *args, a1: Anchor, a2: Anchor):
        super().__init__(*args)
        self.a1 = a1
        self.a2 = a2
        self.dist_vect = {}
        self._update_distance()

    def corner_moved(self):
        p1 = self.a1.get_point()
        p2 = self.a2.get_point()
        p_m = geo.get_mid_point(p1, p2)
        angle = geo.get_angle_2p(p1, p2) + self.dist_vect["angle"]
        x = p_m[0] + math.cos(angle) * self.dist_vect["dist"]
        y = p_m[1] + math.sin(angle) * self.dist_vect["dist"]
        self.setPos(self._off_pos(x), self._off_pos(y))

    def _update_distance(self):
        p1 = self.a1.get_point()
        p2 = self.a2.get_point()
        angle, dist = geo.get_angle_and_dist_from_line(p1, p2, self.get_point())
        self.dist_vect = {"angle": angle, "dist": dist}

    def mouseMoveEvent(self, event):
        p_oa, p_oc, p_uc = self._get_event_points(event)
        p1, p2 = self.a1.get_point(), self.a2.get_point()
        v = geo.get_vector_projected_on_axis(p1, p2, p_oc, p_uc)
        p = geo.get_point_moved_by_vector(p_oa, v)
        self.setPos(p[0], p[1])
        self.rect.update_lines()
        self._update_distance()
        self.center_point.setPos(0, 0)


class Line(QGraphicsLineItem):

    def __init__(self, a_radius, width):
        super().__init__(0, 0, 0, 0)
        self.a_size = a_radius
        pen = QPen()
        pen.setWidth(width)
        pen.setColor(QtGui.QColor(50, 50, 50))
        pen.setStyle(QtCore.Qt.DashLine)
        self.setPen(pen)

    def update_pos(self, p1, p2, p1_is_anchor, p2_is_anchor):
        angle = geo.get_angle_2p(p1, p2)
        r = self.a_size / 2
        dx = math.cos(angle) * r
        dy = math.sin(angle) * r
        ax, ay, bx, by = p1[0], p1[1], p2[0], p2[1]
        if p1_is_anchor:
            ax += dx
            ay += dy
        if p2_is_anchor:
            bx -= dx
            by -= dy
        self.setLine(ax, ay, bx, by)


class SelectionBox:

    def __init__(self, scene, points=None):
        self.points = points
        self.scene = scene
        self.a_radius = 100
        self.l_width = 10
        self.lines = [Line(self.a_radius, self.l_width) for _ in range(5)]
        self.anchors = []
        self.is_ready = False
        if self.points is not None:
            self.is_ready = True
            self.anchors = self._make_anchors_from_points(self.points)
            for i in self.anchors:
                self.scene.addItem(i)
        self.update_lines()
        for i in self.lines:
            self.scene.addItem(i)

    def _make_anchors_from_points(self, points):
        point_mid = [stat.mean([points[2][0], points[3][0]]),
                     stat.mean([points[2][1], points[3][1]])]
        anchor_c1 = CornerAnchor(points[0], self.a_radius, self, Qt.red)
        anchor_c2 = CornerAnchor(points[1], self.a_radius, self, Qt.red)
        anchor_s = SlideAnchor(point_mid, self.a_radius, self, Qt.blue,
                               a1=anchor_c1, a2=anchor_c2)
        anchor_c1.add_slide_anchor(anchor_s)
        anchor_c2.add_slide_anchor(anchor_s)
        return [anchor_c1, anchor_c2, anchor_s]

    def _make_anchor_from_event(self, x, y):
        if len(self.anchors) < 2:
            anchor = CornerAnchor([x, y], self.a_radius, self, Qt.red)
        else:
            anchor = SlideAnchor([x, y], self.a_radius, self, Qt.blue, a1=self.anchors[0], a2=self.anchors[1])
            self.anchors[0].add_slide_anchor(anchor)
            self.anchors[1].add_slide_anchor(anchor)
        return anchor

    def add_anchor(self, x, y):
        anchor = self._make_anchor_from_event(x, y)
        self.anchors.append(anchor)
        if len(self.anchors) == 3:
            self.is_ready = True
        self.scene.addItem(anchor)
        self.update_lines()

    def drop_all(self):
        for i in self.anchors:
            self.scene.removeItem(i)
        for i in self.lines:
            self.scene.removeItem(i)

    def get_points_from_anchors(self):
        return [x.get_point() for x in self.anchors]

    def update_lines(self):
        if self.is_ready:
            points = geo.get_corners_from_anchors(*self.get_points_from_anchors())
            points.insert(3, self.anchors[2].get_point())
            for idx, line in enumerate(self.lines):
                i = idx % 5
                j = (idx + 1) % 5
                line.update_pos(points[i], points[j], i in [0, 1, 3], j in [0, 1, 3])
