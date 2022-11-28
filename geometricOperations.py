import math


def get_distance_to_point(p1, p2, p3):
    x0, y0 = p3[0], p3[1]
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    top = -(x2 - x1) * (y1 - y0) + (x1 - x0) * (y2 - y1)
    bot = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    return top / bot


def get_corners_from_anchors(p1, p2, p3):
    v1 = p1[0] - p2[0]
    v2 = p1[1] - p2[1]
    d1 = get_distance_to_point(p1, p2, p3)
    d2 = math.sqrt(v1 ** 2 + v2 ** 2)
    ratio = d1 / d2
    p3 = [p2[0] + v2 * ratio, p2[1] - v1 * ratio]
    p4 = [p1[0] + v2 * ratio, p1[1] - v1 * ratio]
    return [p1, p2, p3, p4]


def get_angle(p1, p2):
    x0, y0 = p1[0], p1[1]
    x1, y1 = p2[0], p2[1]
    return math.atan2(y1 - y0, x1 - x0)

