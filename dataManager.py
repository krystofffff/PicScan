import os.path
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QSizePolicy

import graphicOperations as Go

_files = []
_cutouts = {}
_canvas = None
_current_file = ""


class Cutout:
    def __init__(self, img, enabled):
        self.img = img
        self.disabledImg = Go.getDisabledImage(img)
        self.enabled = enabled


def getCutouts():
    return _cutouts


def getCanvas():
    return _canvas


def saveCutouts():
    for idx, img in _cutouts.items():
        if img.enabled:
            cv2.imwrite(("./output/img_" + str(idx) + ".jpg"), img.img)
    print("DONE")


def getNewCanvas():
    global _canvas
    _canvas = _loadImage(getNextImage())


def generateCutouts():
    global _cutouts
    cts = Go.getCutOutImages(_canvas)
    _cutouts = {i: Cutout(img, True) for i, img in enumerate(cts)}


def _loadImage(url):
    stream = open(url, "rb")
    bts = bytearray(stream.read())
    nparray = np.asarray(bts, dtype=np.uint8)
    bgrImage = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
    return bgrImage


def clearData():
    global _files, _cutouts, _canvas
    _files = []
    _cutouts = dict()
    _canvas = None


def addFile(path):
    global _files
    for i in path:
        url = i.path()[1:]
        if _isFolder(url):
            _addDirContent(url)
        else:
            _files.append(url)


def _isImage(path):
    fileName = path[path.rfind(".") + 1:]
    if fileName in ["bmp", "jpeg", "jpg", "tiff", "png"]:
        return True
    else:
        return False


def _isFolder(path):
    return os.path.isdir(path)


def isEmpty():
    global _files
    if len(_files) == 0:
        return True
    else:
        return False


def _addDirContent(file):
    global _files
    a = [(file + "/" + x) for x in os.listdir(file)]
    _files += a


def getNextImage():
    global _files, _current_file
    if isEmpty():
        return None
    else:
        _current_file = _files.pop(0)
        if _isFolder(_current_file):
            _addDirContent(_current_file)
            return getNextImage()
        else:
            if _isImage(_current_file):
                return _current_file
            else:
                return getNextImage()


def rotateCutout(idx):
    _cutouts[idx].img = Go.rotateImage(_cutouts[idx].img)
    _cutouts[idx].disabledImg = Go.rotateImage(_cutouts[idx].disabledImg)


def zoomImage(idx):
    dialog = QDialog()
    dialog.setWindowTitle("image")
    image = Go.getQPixmap(_cutouts[idx].img)
    downscaled_image = image.scaled(1000, 800, Qt.KeepAspectRatio)

    label = QLabel()
    label.setPixmap((downscaled_image))
    label.setMinimumSize(label.sizeHint())

    vbox = QVBoxLayout()
    vbox.addWidget(label)

    dialog.setLayout(vbox)
    dialog.exec_()


def toggleCutout(key):
    _cutouts.get(key).enabled = not _cutouts.get(key).enabled


def getFileName():
    global _current_file
    s = _current_file.split("/")
    return s[-1]
