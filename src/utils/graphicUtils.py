import math
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import src.utils.geometricUtils as Geo
import src.managers.nnRotManager as Nm
import src.managers.configManager as Cm


# def _show(img):
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.show()


def rotate_image(img, n=0):
    return cv2.rotate(img, n)


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


def load_image(url):
    stream = open(url, "rb")
    bts = bytearray(stream.read())
    nparray = np.asarray(bts, dtype=np.uint8)
    bgr_image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
    return bgr_image


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
        s = subimage(img, i)
        images.append(s)
    if Cm.get_nn_loading():
        images = _fix_rotation(images)
    return images, points


def _fix_rotation(images):
    preds = Nm.get_predictions(images)
    for idx, pred in enumerate(preds):
        if not pred == 3:
            images[idx] = rotate_image(images[idx], pred)
    return images


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


# Albumentations copied

def normalize_cv2(img, mean, denominator):
    if mean.shape and len(mean) != 4 and mean.shape != img.shape:
        mean = np.array(mean.tolist() + [0] * (4 - len(mean)), dtype=np.float64)
    if not denominator.shape:
        denominator = np.array([denominator.tolist()] * 4, dtype=np.float64)
    elif len(denominator) != 4 and denominator.shape != img.shape:
        denominator = np.array(denominator.tolist() + [1] * (4 - len(denominator)), dtype=np.float64)

    img = np.ascontiguousarray(img.astype("float32"))
    cv2.subtract(img, mean.astype(np.float64), img)
    cv2.multiply(img, denominator.astype(np.float64), img)
    return img


def normalize_numpy(img, mean, denominator):
    img = img.astype(np.float32)
    img -= mean
    img *= denominator
    return img


def normalize(img, mean, std, max_pixel_value=255.0):
    mean = np.array(mean, dtype=np.float32)
    mean *= max_pixel_value

    std = np.array(std, dtype=np.float32)
    std *= max_pixel_value

    denominator = np.reciprocal(std, dtype=np.float32)

    if img.ndim == 3 and img.shape[-1] == 3:
        return normalize_cv2(img, mean, denominator)
    return normalize_numpy(img, mean, denominator)


def augment(img):
    mean = 0
    std = 1.0
    max_pixel_value = 255.0

    return normalize(img, mean, std, max_pixel_value)
