import os.path
import time

import cv2

import src.managers.config_manager as cm
import src.managers.hash_manager as hm
import src.utils.graphic_utils as gra

_files = []
_cutouts = []
_canvas = None
_current_file = ""
_file_counter = 0
_file_count = 0
_process_timer = 0
OUTPUT_FORMATS = [".jpg", ".png"]
INPUT_FORMATS = ["bmp", "jpeg", "jpg", "tiff", "png"]


class Cutout:
    def __init__(self, img, points):
        self.img = img
        self.disabled_img = gra.get_disabled_image(img)
        self.enabled = True
        self.points = points


def save_cutouts():
    global OUTPUT_FORMATS, _file_counter, _cutouts
    output_format = OUTPUT_FORMATS[cm.get_output_format()]
    output_folder = cm.get_output_folder()
    for idx, co in enumerate(_cutouts):
        if co.enabled:
            path = f"{output_folder}/img_{_file_counter}_{idx}{output_format}"
            if cm.get_duplicity_mode() == 1:
                hm.add_to_hashes(co.img, path)
            cv2.imwrite(path, co.img)


def set_file_count(paths):
    global _file_count
    _file_count = 0
    stack = paths.copy()
    while not len(stack) == 0:
        f = stack.pop(-1)
        if _is_folder(f):
            stack += [(f + "/" + x) for x in os.listdir(f)]
        elif _is_image(f):
            _file_count += 1


def process_next_image():
    global _file_counter, _process_timer
    if not is_empty():
        t = time.perf_counter()
        _file_counter += 1
        generate_canvas()
        generate_cutouts()
        _process_timer += time.perf_counter() - t


def generate_canvas():
    global _canvas
    file = _get_next_file()
    _canvas = gra.load_image(file)


def generate_cutouts():
    global _cutouts
    cts, points = gra.get_cut_out_images(_canvas)
    _cutouts = [Cutout(img, points[i]) for i, img in enumerate(cts)]


def any_disabled_cutouts():
    global _cutouts
    for i in _cutouts:
        if not i.enabled:
            return True
    return False


def clear_data():
    global _files, _cutouts, _canvas, _file_counter, _current_file, _file_count, _process_timer
    _file_counter = 0
    _files = []
    _cutouts = []
    _canvas = None
    _current_file = ""
    _file_counter = 0
    _file_count = 0
    _process_timer = 0


def add_file(path):
    global _files
    for i in path:
        if _is_folder(i):
            _add_dir_content(i)
        else:
            _files.append(i)


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
    global _cutouts
    _cutouts[idx].img = gra.rotate_image(_cutouts[idx].img)
    _cutouts[idx].disabled_img = gra.rotate_image(_cutouts[idx].disabled_img)


def toggle_cutout(idx):
    _cutouts[idx].enabled = not _cutouts[idx].enabled


def get_file_name():
    global _current_file
    s = _current_file.split("/")
    return s[-1]


def update_cutout(idx, p):
    points = [[x] for x in p]
    get_cutouts()[idx] = Cutout(gra.subimage(get_canvas(), points), points)


def get_file_counter():
    return _file_counter


def get_cutouts():
    return _cutouts


def get_cutout_points(idx):
    return _cutouts[idx].points


def get_canvas():
    return _canvas


def get_file_count():
    return _file_count


def get_process_timer():
    return _process_timer
