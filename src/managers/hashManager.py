import os
import cv2
import numpy as np

from definitions import HASHES_PATH
import src.utils.graphicUtils as Gra

_hashes = []
_hasher = cv2.img_hash.PHash_create()

SIMILARITY_THRESHOLD = 0.75


class HashImage:
    def __init__(self, img, h):
        self.h = h
        self.img = img
        self.disabled_img = Gra.get_disabled_image(img)
        self.enabled = True


def clear_hashes():
    global _hashes
    _hashes = []


def load_imgs_for_simui_beta():
    f = "C:/Users/Dumar/PycharmProjects/Annual-project-1/test/testingImages/sim_ims"
    stack = [(f + "/" + x) for x in os.listdir(f)]
    imgs = [cv2.imread(x) for x in stack]
    return imgs


def _get_hash(img):
    return _hasher.compute(img)


def _get_similarity(h1, h2):
    s = _hasher.compare(h1, h2)
    return 1 - (s / 64.0)


def _is_similar(h1, h2):
    return _get_similarity(h1, h2) >= SIMILARITY_THRESHOLD


def add_to_hashes(img, path):
    global _hashes
    h = {"hash": _get_hash(img), "path": path, "sims": []}
    for i in _hashes:
        if _is_similar(i["hash"], h["hash"]):
            h["sims"].append(i)
            i["sims"].append(h)
    _hashes.append(h)


def remove_non_similar():
    global _hashes
    for i in reversed(_hashes):
        if len(i["sims"]) == 0:
            _hashes.remove(i)


# TODO move to file utils ?
def _load_image(url):
    stream = open(url, "rb")
    bts = bytearray(stream.read())
    nparray = np.asarray(bts, dtype=np.uint8)
    bgr_image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
    return bgr_image


def _get_hashimages(h):
    res = []
    for i in h["sims"]:
        img = _load_image(i["path"])
        res.append(HashImage(img, i))
    return res
