import os.path
import cv2
import numpy as np
from src.utils import graphicUtils as Gra
import src.managers.configManager as Cm
import src.managers.hashManager as Hm


_files = []
_cutouts = {}
_canvas = None
_current_file = ""
_file_counter = 0
_saved_cutouts_counter = 0
_discarded_cutouts_counter = 0
OUTPUT_FORMATS = [".jpg", ".png"]
INPUT_FORMATS = ["bmp", "jpeg", "jpg", "tiff", "png"]


class Cutout:
    def __init__(self, img, points):
        self.img = img
        self.disabled_img = Gra.get_disabled_image(img)
        if Cm.get_similarity_mode() == 0:
            self.enabled = True
        else:
            self.enabled = not Hm.image_is_similar(img)
        self.points = points


def save_cutouts():
    global OUTPUT_FORMATS, _file_counter, _saved_cutouts_counter, _discarded_cutouts_counter
    Hm.save_hashes()
    output_format = OUTPUT_FORMATS[Cm.get_output_format()]
    output_folder = Cm.get_output_folder()
    for idx, img in _cutouts.items():
        if img.enabled:
            _saved_cutouts_counter += 1
            # TODO IF OUTPUT FOLDER IS MISSING ? (eg. AFTER BUILD)
            cv2.imwrite(f"{output_folder}/img_{_file_counter}_{idx}{output_format}", img.img)
        else:
            _discarded_cutouts_counter += 1


def process_next_image():
    global _file_counter
    if not is_empty():
        _file_counter += 1
        generate_canvas()
        generate_cutouts()


def generate_canvas():
    global _canvas
    file = _get_next_file()
    _canvas = _load_image(file)


def generate_cutouts():
    global _cutouts
    cts, points = Gra.get_cut_out_images(_canvas)
    # TODO DICT TO ARRAY (DICT NOT NEEDED ANYMORE - no removing)
    _cutouts = {i: Cutout(img, points[i]) for i, img in enumerate(cts)}


def any_disabled_cutouts():
    global _cutouts
    for i in _cutouts.values():
        if not i.enabled:
            return True
    return False


def _load_image(url):
    stream = open(url, "rb")
    bts = bytearray(stream.read())
    nparray = np.asarray(bts, dtype=np.uint8)
    bgr_image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
    return bgr_image


def clear_data():
    global _files, _cutouts, _canvas, _file_counter, _saved_cutouts_counter, _discarded_cutouts_counter
    _file_counter = 0
    _files = []
    _cutouts = {}
    _canvas = None
    _saved_cutouts_counter = 0
    _discarded_cutouts_counter = 0


def add_file(path):
    global _files
    for i in path:
        url = i.path()[1:]
        if _is_folder(url):
            _add_dir_content(url)
        else:
            _files.append(url)


def _is_image(path):
    global INPUT_FORMATS
    file_name = path[path.rfind(".") + 1:]
    if file_name in INPUT_FORMATS:
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


def _get_next_file():
    global _files, _current_file
    if is_empty():
        return None
    else:
        _current_file = _files.pop(0)
        if _is_folder(_current_file):
            _add_dir_content(_current_file)
            return _get_next_file()
        else:
            if _is_image(_current_file):
                return _current_file
            else:
                return _get_next_file()


def rotate_cutout(idx):
    _cutouts[idx].img = Gra.rotate_image(_cutouts[idx].img)
    _cutouts[idx].disabled_img = Gra.rotate_image(_cutouts[idx].disabled_img)


def toggle_cutout(idx):
    _cutouts[idx].enabled = not _cutouts[idx].enabled


def get_file_name():
    global _current_file
    s = _current_file.split("/")
    return s[-1]


def update_cutout(idx, p):
    points = [[x] for x in p]
    get_cutouts()[idx] = Cutout(Gra.subimage(get_canvas(), points), points)


def get_file_counter():
    return _file_counter


def get_discarded_cutouts_counter():
    return _discarded_cutouts_counter


def get_saved_cutouts_counter():
    return _saved_cutouts_counter


def get_cutouts():
    return _cutouts


def get_cutout_points(idx):
    return _cutouts[idx].points


def get_canvas():
    return _canvas
