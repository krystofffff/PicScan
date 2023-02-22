import math
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import src.operations.geometricOperations as Geo


# TODO DELETE ?
# def resize_image_to_fit(img, shape):
#     wc, hc = shape.width(), shape.height()
#     wi, hi = len(img[0]), len(img)
#     print(wi, hi)
#     print(img.shape())
#     if ((wc * 1.0) / hc) >= ((wi * 1.0) / hi):
#         f = (hc * 1.0) / hi
#     else:
#         f = (wc * 1.0) / wi
#     return cv2.resize(img, (0, 0), fx=f, fy=f)


# def _show(img):
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.show()


def rotate_image(img):
    return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


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
        p1 = points[i % 4][0]
        p2 = points[(i + 1) % 4][0]
        p3 = points[(i + 2) % 4][0]
        angle = Geo.get_angle_3p(p1, p2, p3)
        angle = math.degrees(Geo.pos_angle(angle)) % 180
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


def get_cut_out_images(image):
    img, points = _find_rectangles(image)
    images = []
    for i in points:
        images.append(subimage(img, i))
    return images, points


def get_disabled_image(img):
    img = np.copy(img)
    c = 25
    w = min(img.shape[1], img.shape[0]) // 8
    cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (c, c, 255, 255), w)
    cv2.line(img, (img.shape[1], 0), (0, img.shape[0]), (c, c, 255, 255), w)
    return img


def subimage(image, corners):
    image = image.copy()

    c_width, c_height, c_center, theta = Geo.get_specs_from_corners(corners)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    rot = _get_rotated_image(image, theta)

    h, w = image.shape[:2]
    oi_center = (w / 2, h / 2)
    h, w = rot.shape[:2]
    ni_center = (w / 2, h / 2)
    v = Geo.get_vector_between_points(oi_center, c_center)
    vv = Geo.get_point_rotated_around_point([0, 0], v, -theta)
    p = Geo.get_point_moved_by_vector(ni_center, vv)
    p = [int(p[0]), int(p[1])]
    p = Geo.get_point_moved_by_vector(p, [-c_width // 2, -c_height // 2])

    cutout = _cutout_image(rot, p, c_width, c_height, h, w)

    return cutout


def _cutout_image(img, corner, c_width, c_height, i_h, i_w):
    zer = np.zeros((c_height, c_width, 4), np.uint8)

    x, y = corner[0], corner[1]
    h_max = min(i_h, y + c_height)
    w_max = min(i_w, x + c_width)
    x_min = max(0, x)
    y_min = max(0, y)

    if h_max >= 0 and w_max >= 0:
        zer[y_min - y:h_max - y, x_min - x:w_max - x] = img[y_min:h_max, x_min:w_max]

    return zer


def _get_rotated_image(image, angle):
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)
    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]
    rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h), borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(0, 0, 0, 0))
    # rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h))
    return rotated_mat


def get_qpixmap(img):
    height, width, color_bytes = img.shape
    bytes_per_line = color_bytes * width
    if color_bytes == 4:
        conv_format = cv2.COLOR_BGRA2RGBA
        qimage_format = QImage.Format_RGBA8888
    else:
        conv_format = cv2.COLOR_BGR2RGB
        qimage_format = QImage.Format_RGB888
    img = cv2.cvtColor(img, conv_format)
    q_img = QImage(img.data, width, height, bytes_per_line, qimage_format)

    return QPixmap(q_img)
