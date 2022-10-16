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


def calcDistance(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def addRadius(points):
    minimum = max([HEIGHT, WIDTH])
    last = points[len(points) - 1]
    for jdx, j in enumerate(points):
        if len(points) - 1 == jdx:
            continue
        else:
            dist = int(calcDistance(j[0], j[1], last[0], last[1]) - j[2])
            minimum = min([dist, minimum])
    minimum = min([minimum, last[0], last[1], HEIGHT - last[1], WIDTH - last[0]])
    last.append(minimum)


def getPoints(count):
    freeSpots = [[x, y] for y in range(MIN_RADIUS, HEIGHT - MIN_RADIUS, GRID_SIZE) for x in
                 range(MIN_RADIUS, WIDTH - MIN_RADIUS, GRID_SIZE)]
    points = []
    sketch = np.zeros((HEIGHT, WIDTH, 1), dtype=np.byte)
    while len(points) < count:
        p = getNewPoint(freeSpots)
        points.append(p)
        addRadius(points)
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


def getNewPoint(arr):
    idx = random.randrange(len(arr))
    return [arr[idx][0], arr[idx][1]]


def show(img):
    plt.imshow(img)
    plt.show()


def rotate(points, angle):
    w = len(points[0])
    h = len(points)
    x = w // 2
    y = h // 2
    rotate_matrix = cv2.getRotationMatrix2D(center=(x, y), angle=angle, scale=1)
    return cv2.warpAffine(src=points, M=rotate_matrix, dsize=(w, h))


def getImageAndMask(img, radius, angle):
    w, h = getWidthAndHeight(img)
    m = np.zeros((h, w, 3), dtype=np.uint8)
    m[::] = (255, 255, 255)
    transformed = scaledAndRotated(img, radius, angle)
    mask = scaledAndRotated(m, radius, angle)
    return transformed, mask


def scaledAndRotated(img, radius, angle):
    w_i, h_i = getWidthAndHeight(img)
    f = (radius * 2) / int(math.sqrt(w_i ** 2 + h_i ** 2))
    scaled = cv2.resize(img, None, fx=f, fy=f)
    w_sc, h_sc = getWidthAndHeight(scaled)
    m = int(math.sqrt(w_sc ** 2 + h_sc ** 2))
    sq = np.zeros((m, m, 3), dtype=np.uint8)
    fTop = (m - h_sc) // 2
    fLeft = (m - w_sc) // 2
    sq[fTop:fTop + h_sc, fLeft:fLeft + w_sc] = scaled
    return rotate(sq, angle)


def getWidthAndHeight(img):
    return len(img[0]), len(img)


def addToCanvas(canvas, image, point, angle):
    img, mask = getImageAndMask(image, point[2], angle)
    w, h = getWidthAndHeight(img)
    for i in range(h):
        for j in range(w):
            if mask[i][j][0] == 255:
                canvas[point[1] - h // 2 + i][point[0] - w // 2 + j] = img[i][j]


def getRandomImage():
    w = random.randrange(100, 500)
    h = random.randrange(100, 500)
    url = 'https://random.imagecdn.app/' + str(w) + "/" + str(h) + "/"
    response = requests.get(url)
    print(response)
    img = Image.open(BytesIO(response.content))
    pix = np.asarray(img)
    # i = cv2.imread("01.png")
    return pix


def generateCanvas(visualize):
    canvas = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    canvas[:] = (255, 255, 255)
    points = getPoints(5)
    for i in points:
        # cv2.circle(canvas, (i[0], i[1]), i[2], (255, 0, 0), 1)
        addToCanvas(canvas, getRandomImage(), i, random.randrange(360))
    if visualize:
        show(canvas)
    return canvas

a = generateCanvas(True)
cv2.imwrite("./pic_scan/backend/tests/scans/output.jpg", cv2.cvtColor(a, cv2.COLOR_RGB2BGR))
