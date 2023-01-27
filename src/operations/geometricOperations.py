import math
import statistics as stat
import numpy as np


def _get_distance_from_line_to_point(p1, p2, p3):
    x0, y0 = p3[0], p3[1]
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    top = -(x2 - x1) * (y1 - y0) + (x1 - x0) * (y2 - y1)
    bot = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    return top / bot


def get_corners_from_anchors(p1, p2, p3):
    v1 = p1[0] - p2[0]
    v2 = p1[1] - p2[1]
    d1 = _get_distance_from_line_to_point(p1, p2, p3)
    d2 = math.sqrt(v1 ** 2 + v2 ** 2)
    ratio = d1 / d2
    p3 = [p2[0] + v2 * ratio, p2[1] - v1 * ratio]
    p4 = [p1[0] + v2 * ratio, p1[1] - v1 * ratio]
    return [p1, p2, p3, p4]


def get_angle_2p(p1, p2):
    x0, y0 = p1[0], p1[1]
    x1, y1 = p2[0], p2[1]
    return math.atan2(y1 - y0, x1 - x0)


def get_angle_3p(a, b, c):
    ang = get_angle_2p(b, c) - get_angle_2p(b, a)
    return ang


def pos_angle(ang):
    return ang + math.tau if ang < 0 else ang


def get_mid_point(p1, p2):
    x = int(stat.mean([p1[0], p2[0]]))
    y = int(stat.mean([p1[1], p2[1]]))
    return [x, y]


def _get_diffs(p1, p2):
    diff_x = p2[0] - p1[0]
    diff_y = p2[1] - p1[1]
    return diff_x, diff_y


def get_vector_projected_on_axis(p1, p2, p_o, p_n):
    diff_x, diff_y = _get_diffs(p_o, p_n)
    angle1 = get_angle_2p(p1, p2) - math.pi / 2
    angle2 = get_angle_2p(p_o, p_n)
    angle_fin = angle2 - angle1
    length = math.sqrt(diff_x ** 2 + diff_y ** 2)
    a = math.cos(angle_fin) * length
    return [math.cos(angle1) * a, math.sin(angle1) * a]


def get_angle_and_dist_from_line(p1, p2, p):
    p_p = get_point_on_line(p1, p2, p)
    v = get_vector_between_points(p_p, p)
    angle = math.atan2(v[1], v[0]) - get_angle_2p(p1, p2)
    dist = math.sqrt(v[0] ** 2 + v[1] ** 2)
    return angle, dist


def get_point_on_line(a, b, p):
    a = np.array(a)
    b = np.array(b)
    p = np.array(p)
    ap = p - a
    ab = b - a
    result = a + np.dot(ap, ab) / np.dot(ab, ab) * ab
    return result


def get_vector_between_points(p1, p2):
    return [*_get_diffs(p1, p2)]


def get_distance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


def get_point_moved_by_vector(p, v):
    return [p[0] + v[0], p[1] + v[1]]


def get_point_rotated_around_point(center, p, angle):
    point = np.array(p)
    origin = np.array(center)
    angle = math.radians(angle)
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    rotated_point = np.dot(rotation_matrix, point - origin) + origin
    return [int(rotated_point[0]), int(rotated_point[1])]
