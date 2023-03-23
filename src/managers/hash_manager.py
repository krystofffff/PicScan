import os

import cv2

import src.utils.graphic_utils as gra

_hashes = []
_hash_images = []
_hasher = cv2.img_hash.PHash_create()

SIMILARITY_THRESHOLD = 0.75


class HashImage:
    def __init__(self, img, h, sim):
        self.h = h
        self.img = img
        self.disabled_img = gra.get_disabled_image(img)
        self.enabled = True
        self.sim = sim

    def toggle(self):
        self.enabled = not self.enabled

    def get_img(self):
        return self.img if self.enabled else self.disabled_img


class Hash:
    def __init__(self, h, path):
        self.h = h
        self.path = path
        self.sims = []


def process_hash_images(is_accepted):
    for i in _hash_images:
        if not i.enabled:
            os.remove(i.h.path)
            _remove_from_hashes(i.h)
    if not is_accepted:
        os.remove(_hash_images[0].h.path)
    _remove_from_hashes(_hash_images[0].h)


def _remove_from_hashes(h):
    global _hashes
    sims = [x["h"] for x in h.sims]
    for i in sims:
        i.sims = [x for x in i.sims if x["h"] is not h]
        if not i.sims:
            _hashes.remove(i)
    if h.sims:
        _hashes.remove(h)


def clear_hashes():
    global _hashes
    _hashes = []


def build_new_hashimages(h=None):
    if h is None:
        _build_hashimages(_hashes[0])
    else:
        _build_hashimages(h)


def _get_hash(img):
    return _hasher.compute(img)


def _get_similarity(h1, h2):
    s = _hasher.compare(h1, h2)
    return 1 - (s / 64.0)


def add_to_hashes(img, path):
    global _hashes
    new_h = Hash(_get_hash(img), path)
    for i in _hashes:
        s = _get_similarity(i.h, new_h.h)
        if s >= SIMILARITY_THRESHOLD:
            new_h.sims.append({"h": i, "s": s})
            i.sims.append({"h": new_h, "s": s})
    _hashes.append(new_h)


def remove_non_similar():
    global _hashes
    for i in reversed(_hashes):
        if len(i.sims) == 0:
            _hashes.remove(i)


def get_hashimages():
    return _hash_images


def _build_hashimages(h):
    global _hash_images
    res = [HashImage(gra.load_image(h.path), h, 0)]
    hs = sorted(h.sims, key=lambda x: x["s"], reverse=True)
    for i in hs:
        hsh = i["h"]
        img = gra.load_image(hsh.path)
        res.append(HashImage(img, hsh, i["s"]))
    _hash_images = res


def is_empty():
    return len(_hashes) == 0
