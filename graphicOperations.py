import math
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


def loadImage(url):
    stream = open(url, "rb")
    bts = bytearray(stream.read())
    nparray = np.asarray(bts, dtype=np.uint8)
    bgrImage = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
    return bgrImage


def rotateImage(img, angle):
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))


def getNormalImage(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def resizeImageToFit(img, shape):
    wc, hc = shape.width(), shape.height()
    wi, hi = len(img[0]), len(img)
    if ((wc * 1.0) / hc) >= ((wi * 1.0) / hi):
        f = (hc * 1.0) / hi
    else:
        f = (wc * 1.0) / wi
    return cv2.resize(img, (0, 0), fx=f, fy=f)


def show(img):
    plt.imshow(getNormalImage(img))
    plt.show()


def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def findRectangles(img):
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
            if isValidRectangle(approx):
                # r, g, b = random.randint(25, 230), random.randint(25, 230), random.randint(25, 230)
                # img = cv2.drawContours(img, [approx], -1, (r, g, b), 25)
                corners.append(approx)
    return img, corners


def isValidRectangle(points):
    counter = 0
    lastRight = None
    for i in range(4):
        angle = getAngle(points[i % 4][0], points[(i + 1) % 4][0], points[(i + 2) % 4][0]) % 180
        if abs(90 - angle) > 2:
            counter += 1
        else:
            lastRight = (i + 1) % 4
    if counter == 4:
        return False
    elif counter in (2, 3):
        repairRectangle(points, lastRight)
    return True


def repairRectangle(points, last_right_index):
    index = (last_right_index + 2) % 4
    v_x = points[(index + 3) % 4][0][1] - points[(index + 2) % 4][0][1]
    v_y = points[(index + 3) % 4][0][0] - points[(index + 2) % 4][0][0]
    newPoint = [points[(index + 1) % 4][0][0] + v_y, points[(index + 1) % 4][0][1] + v_x]
    points[index][0] = newPoint


def getDistance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


def getAngleToAxis(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def cutOutImages(img, points):
    images = []
    for i in points:
        images.append(subimage(img, i))
    return images


def getIndexOfBottom(corners):
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


def subimage(image, corners):
    sx = sy = 0
    index = getIndexOfBottom(corners)
    # image = cv2.circle(image, (corners[index][0][0], corners[index][0][1]), 25, (100,), -1)
    width = int(getDistance(corners[index][0], corners[(index + 1) % 4][0]))
    height = int(getDistance(corners[index][0], corners[(index + 3) % 4][0]))
    for point in corners:
        sx += point[0][0]
        sy += point[0][1]
    center = [int(sx / 4.0), int(sy / 4.0)]
    theta = math.degrees(getAngleToAxis(corners[index][0], corners[(index + 1) % 4][0]))
    shape = (image.shape[1], image.shape[0])
    matrix = cv2.getRotationMatrix2D(center=center, angle=theta, scale=1)
    img = cv2.warpAffine(src=image, M=matrix, dsize=shape)
    x = int(center[0] - width / 2)
    y = int(center[1] - height / 2)
    img = img[y:y + height, x:x + width]
    return img


def getQPixmap(img):
    img = getNormalImage(img)
    height, width, channel = img.shape
    bytesPerLine = 3 * width
    qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap(qImg)