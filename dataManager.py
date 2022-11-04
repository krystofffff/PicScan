import os.path
import cv2
import numpy as np
import graphicOperations as Go

_files = []
_cutouts = []
_canvas = None


def getCutouts():
    return _cutouts


def getCanvas():
    return _canvas


def saveCutouts():
    for idx, img in enumerate(_cutouts):
        cv2.imwrite(("./output/img_" + str(idx) + ".jpg"), img)
    print("DONE")


def loadNewCanvas():
    global _canvas
    _canvas = _loadImage(getNextImage())


def generateCutouts():
    global _cutouts
    _cutouts = Go.getCutOutImages(_canvas)


def _loadImage(url):
    stream = open(url, "rb")
    bts = bytearray(stream.read())
    nparray = np.asarray(bts, dtype=np.uint8)
    bgrImage = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
    return bgrImage


def clearData():
    global _files, _cutouts, _canvas
    _files = []
    _cutouts = []
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
    global _files
    if isEmpty():
        return None
    else:
        file = _files.pop(0)
        if _isFolder(file):
            _addDirContent(file)
            return getNextImage()
        else:
            if _isImage(file):
                return file
            else:
                return getNextImage()
