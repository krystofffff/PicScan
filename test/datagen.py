import os

import numpy as np
import math
import cv2
import random
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

HEIGHT = 3508
WIDTH = 2480
MIN_RADIUS = 300
GRID_SIZE = 100


def _calc_distance(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def _add_radius(points):
    minimum = max([HEIGHT, WIDTH])
    last = points[len(points) - 1]
    for jdx, j in enumerate(points):
        if len(points) - 1 == jdx:
            continue
        else:
            dist = int(_calc_distance(j[0], j[1], last[0], last[1]) - j[2])
            minimum = min([dist, minimum])
    minimum = min([minimum, last[0], last[1], HEIGHT - last[1], WIDTH - last[0]])
    last.append(minimum)


def _get_points(count):
    freeSpots = [[x, y] for y in range(MIN_RADIUS, HEIGHT - MIN_RADIUS, GRID_SIZE) for x in
                 range(MIN_RADIUS, WIDTH - MIN_RADIUS, GRID_SIZE)]
    points = []
    sketch = np.zeros((HEIGHT, WIDTH, 1), dtype=np.byte)
    while len(points) < count:
        p = _get_new_point(freeSpots)
        points.append(p)
        _add_radius(points)
        last = len(points) - 1
        cv2.circle(sketch, (points[last][0], points[last][1]), points[last][2] + MIN_RADIUS, 1, cv2.FILLED)
        i = 0
        while i < len(freeSpots):
            pos = freeSpots[i]
            if sketch[pos[1]][pos[0]] == 1:
                del freeSpots[i]
            else:
                i += 1
    return points


def _get_new_point(arr):
    idx = random.randrange(len(arr))
    return [arr[idx][0], arr[idx][1]]


def _show(img):
    plt.imshow(img)
    plt.show()


def _rotate(points, angle):
    w = len(points[0])
    h = len(points)
    x = w // 2
    y = h // 2
    rotate_matrix = cv2.getRotationMatrix2D(center=(x, y), angle=angle, scale=1)
    return cv2.warpAffine(src=points, M=rotate_matrix, dsize=(w, h))


def _get_image_and_mask(img, radius, angle):
    w, h = _get_width_and_height(img)
    m = np.zeros((h, w, 3), dtype=np.uint8)
    m[::] = (255, 255, 255)
    transformed = _scaled_and_rotated(img, radius, angle)
    mask = _scaled_and_rotated(m, radius, angle)
    return transformed, mask


def _scaled_and_rotated(img, radius, angle):
    w_i, h_i = _get_width_and_height(img)
    f = (radius * 2) / int(math.sqrt(w_i ** 2 + h_i ** 2))
    scaled = cv2.resize(img, None, fx=f, fy=f)
    w_sc, h_sc = _get_width_and_height(scaled)
    m = int(math.sqrt(w_sc ** 2 + h_sc ** 2))
    sq = np.zeros((m, m, 3), dtype=np.uint8)
    fTop = (m - h_sc) // 2
    fLeft = (m - w_sc) // 2
    sq[fTop:fTop + h_sc, fLeft:fLeft + w_sc] = scaled
    return _rotate(sq, angle)


def _get_width_and_height(img):
    return len(img[0]), len(img)


def _add_to_canvas(canvas, image, point, angle):
    img, mask = _get_image_and_mask(image, point[2], angle)
    w, h = _get_width_and_height(img)
    for i in range(h):
        for j in range(w):
            if mask[i][j][0] == 255:
                canvas[point[1] - h // 2 + i][point[0] - w // 2 + j] = img[i][j]


def _get_random_image_from_web():
    w = random.randrange(100, 500)
    h = random.randrange(100, 500)
    url = 'https://random.imagecdn.app/' + str(w) + "/" + str(h) + "/"
    response = requests.get(url)
    print(response)
    img = Image.open(BytesIO(response.content))
    pix = np.asarray(img)
    # i = cv2.imread("01.png")
    return pix


def _get_random_image(folder_path):
    imgs = os.listdir(folder_path)
    imgs = [f"{folder_path}/{img}" for img in imgs]
    return np.asarray(cv2.cvtColor(cv2.imread(random.choice(imgs)), cv2.COLOR_BGR2RGB))


def _generate_canvas(folder_path, visualize=False):
    canvas = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    canvas[:] = (255, 255, 255)
    points = _get_points(5)
    imgs = []
    for i in points:
        # cv2.circle(canvas, (i[0], i[1]), i[2], (255, 0, 0), 1)
        img = _get_random_image(folder_path)
        imgs.append(img)
        _add_to_canvas(canvas, img, i, random.randrange(360))
    if visualize:
        _show(canvas)
    return canvas, imgs


def save_canvas_and_imgs(c_path, i_path, input_path):
    canvas, imgs = _generate_canvas(input_path)
    cv2.imwrite(c_path, cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR))
    for idx, i in enumerate(imgs):
        cv2.imwrite(f"{i_path}/{idx}.jpg", cv2.cvtColor(i, cv2.COLOR_RGB2BGR))

