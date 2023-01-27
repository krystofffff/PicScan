import h5py
import numpy as np
import cv2

_hashes = []

SIMILARITY_THRESHOLD = 0.9
HASHES_PATH = "src/data/hashes.hdf5"


def load_hashes():
    global HASHES_PATH, _hashes
    try:
        with h5py.File(HASHES_PATH, "r") as f:
            a_group_key = list(f.keys())[0]
            _hashes = list(f[a_group_key][()])
    except FileNotFoundError:
        pass


def save_hashes():
    global HASHES_PATH, _hashes
    with h5py.File(HASHES_PATH, "w") as data_file:
        data_file.create_dataset("data", data=_hashes)


def image_is_similar(img):
    hs = get_hashes(img)
    for h in hs:
        if _hash_is_similar(h):
            return True
    _add_hashes(hs)
    return False


def get_hashes(img):
    hsh = cv2.img_hash.PHash_create()
    res = []
    for i in range(4):
        rot = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        res.append(hsh.compute(rot)[0])
    return res


def _add_hashes(hs):
    _hashes.extend(hs)


def _hash_is_similar(h):
    global SIMILARITY_THRESHOLD
    for i in _hashes:
        if _get_similarity(i, h) >= SIMILARITY_THRESHOLD:
            return True
    return False


def _get_similarity(h1, h2):
    k = np.bitwise_xor(h1, h2)
    s = 0
    for i in k:
        s += bin(i).count("1")
    return 1 - (s / 64.0)


def get_hash_count():
    return len(_hashes)


def clear_hashes():
    global _hashes
    _hashes = []
    save_hashes()

