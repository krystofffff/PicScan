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
    def __init__(self, img, enabled, points):
        self.img = img
        self.disabled_img = Go.getDisabledImage(img)
        self.enabled = enabled
        self.points = points


def get_cutouts():
    return _cutouts


def get_cutout_points(idx):
    return _cutouts[idx].points


def get_canvas():
    return _canvas


def save_cutouts():
    for idx, img in _cutouts.items():
        if img.enabled:
            cv2.imwrite(("./output/img_" + str(idx) + ".jpg"), img.img)
    print("DONE")


def get_new_canvas():
    global _canvas
    _canvas = _load_image(get_next_image())


def generate_cutouts():
    global _cutouts
    cts, points = Go.getCutOutImages(_canvas)
    _cutouts = {i: Cutout(img, True, points[i]) for i, img in enumerate(cts)}


def _load_image(url):
    stream = open(url, "rb")
    bts = bytearray(stream.read())
    nparray = np.asarray(bts, dtype=np.uint8)
    bgr_image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
    return bgr_image


def clear_data():
    global _files, _cutouts, _canvas
    _files = []
    _cutouts = dict()
    _canvas = None


def add_file(path):
    global _files
    for i in path:
        url = i.path()[1:]
        if _is_folder(url):
            _add_dir_content(url)
        else:
            _files.append(url)


def _is_image(path):
    file_name = path[path.rfind(".") + 1:]
    if file_name in ["bmp", "jpeg", "jpg", "tiff", "png"]:
        return True
    else:
        return False


def _is_folder(path):
    return os.path.isdir(path)


def is_empty():
    global _files
    if len(_files) == 0:
        return True
    else:
        return False


def _add_dir_content(file):
    global _files
    a = [(file + "/" + x) for x in os.listdir(file)]
    _files += a


def get_next_image():
    global _files, _current_file
    if is_empty():
        return None
    else:
        _current_file = _files.pop(0)
        if _is_folder(_current_file):
            _add_dir_content(_current_file)
            return get_next_image()
        else:
            if _is_image(_current_file):
                return _current_file
            else:
                return get_next_image()


def rotate_cutout(idx):
    _cutouts[idx].img = Go.rotateImage(_cutouts[idx].img)
    _cutouts[idx].disabled_img = Go.rotateImage(_cutouts[idx].disabled_img)


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


def toggle_cutout(key):
    _cutouts.get(key).enabled = not _cutouts.get(key).enabled


def get_file_name():
    global _current_file
    s = _current_file.split("/")
    return s[-1]


def update_coutout(idx, p):
    points = [[x] for x in p]
    get_cutouts()[idx] = Cutout(Go._subimage(get_canvas(), points), get_cutouts()[idx].enabled, points)