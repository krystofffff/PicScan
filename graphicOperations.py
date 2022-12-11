import math
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import geometricOperations as Geo


def rotate_image(img):
    return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


def _get_rotated_point(point, center, angle):
    angle = math.radians(angle)
    ox, oy = center[0], center[1]
    px, py = point[0], point[1]
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def resize_image_to_fit(img, shape):
    wc, hc = shape.width(), shape.height()
    wi, hi = len(img[0]), len(img)
    if ((wc * 1.0) / hc) >= ((wi * 1.0) / hi):
        f = (hc * 1.0) / hi
    else:
        f = (wc * 1.0) / wi
    return cv2.resize(img, (0, 0), fx=f, fy=f)


def show(img):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


# TODO MERGE WITH GEOMETRIC
def _get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def _find_rectangles(img):
    corners = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        if len(cnt) < 500:
            continue
        hull = cv2.convexHull(cnt)
        approx = cv2.approxPolyDP(curve=hull, epsilon=100, closed=True)
        if len(approx) == 4:
            if _is_valid_rectangle(approx):
                # r, g, b = random.randint(25, 230), random.randint(25, 230), random.randint(25, 230)
                # img = cv2.drawContours(img, [approx], -1, (r, g, b), 25)
                corners.append(approx)
    return img, corners


def _is_valid_rectangle(points):
    counter = 0
    last_right = None
    for i in range(4):
        angle = _get_angle(points[i % 4][0], points[(i + 1) % 4][0], points[(i + 2) % 4][0]) % 180
        if abs(90 - angle) > 2:
            counter += 1
        else:
            last_right = (i + 1) % 4
    if counter == 4:
        return False
    elif counter in (2, 3):
        _repair_rectangle(points, last_right)
    return True


def _repair_rectangle(points, last_right_index):
    index = (last_right_index + 2) % 4
    v_x = points[(index + 3) % 4][0][1] - points[(index + 2) % 4][0][1]
    v_y = points[(index + 3) % 4][0][0] - points[(index + 2) % 4][0][0]
    new_point = [points[(index + 1) % 4][0][0] + v_y, points[(index + 1) % 4][0][1] + v_x]
    points[index][0] = new_point


def _get_distance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


def _get_angle_to_axis(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def get_cut_out_images(image):
    img, points = _find_rectangles(image)
    images = []
    for i in points:
        images.append(subimage(img, i))
    return images, points


def _get_index_of_bottom(corners):
    maximal = corners[0][0][1]
    index = 0
    for idx, i in enumerate(corners):
        temp = max(i[0][1], maximal)
        if temp > maximal:
            index = idx
            maximal = temp
        elif temp == maximal:
            if i[0][0] > corners[index][0][0]:
                index = idx
                maximal = temp
    return index


def get_disabled_image(img):
    img = np.copy(img)
    c = 25
    w = min(img.shape[1], img.shape[0]) // 8
    cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (c, c, 255), w)
    cv2.line(img, (img.shape[1], 0), (0, img.shape[0]), (c, c, 255), w)
    return img


# TODO transparent instead of black
def subimage(image, corners):
    image = image.copy()
    sx = sy = 0
    index = _get_index_of_bottom(corners)
    width = int(_get_distance(corners[index][0], corners[(index + 1) % 4][0]))
    height = int(_get_distance(corners[index][0], corners[(index + 3) % 4][0]))
    for point in corners:
        sx += point[0][0]
        sy += point[0][1]
    c_center = [int(sx / 4.0), int(sy / 4.0)]
    theta = math.degrees(_get_angle_to_axis(corners[index][0], corners[(index + 1) % 4][0]))

    rot = get_rotated_image(image, theta)

    # cv2.imwrite("C:/Users/Dumar/PycharmProjects/Annual-project-1/a.png", rot)

    h, w = image.shape[:2]
    oi_center = (w / 2, h / 2)
    h, w = rot.shape[:2]
    ni_center = (w / 2, h / 2)
    v = Geo.get_vector_between_points(oi_center, c_center)
    vv = Geo.get_point_rotated_around_point([0, 0], v, -theta)
    p = Geo.get_point_moved_by_vector(ni_center, vv)
    p = [int(p[0]), int(p[1])]
    p = Geo.get_point_moved_by_vector(p, [-width // 2, -height // 2])

    x = p[0]
    y = p[1]

    zer = np.zeros((height, width, 3), np.uint8)

    # TODO optimize
    for i in range(x, x+width):
        for j in range(y, y+height):
            if 0 <= j < h and 0 <= i < w:
                zer[j-y][i-x] = rot[j][i]

    return zer


def get_rotated_image(image, angle):
    height, width = image.shape[:2]
    image_center = (width/2, height/2)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    # rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h), borderMode=cv2.BORDER_CONSTANT,
    #                              borderValue=(0, 0, 0, 0))
    rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h))
    return rotated_mat


def get_qpixmap(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape
    bytes_per_line = 3 * width
    q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return QPixmap(q_img)
