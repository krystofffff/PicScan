import json
import copy
import os.path
from datetime import datetime

from definitions import CONFIG_PATH

_config = {}
_temp_config = {}
_temp_output_folder = None


def get_temp_output_folder():
    return _temp_output_folder


def set_temp_output_folder():
    global _temp_output_folder
    if _temp_output_folder is None:
        now = datetime.now()
        t = now.strftime("%Y-%m-%d-%H-%M-%S")
        _temp_output_folder = f"{get_output_folder()}/{t}"
        os.makedirs(_temp_output_folder)


def clear_temp_output_folder():
    global _temp_output_folder
    _temp_output_folder = None


def load_config():
    global _config
    with open(CONFIG_PATH, 'r') as f:
        _config = json.load(f)


def create_temp_config():
    global _temp_config, _config
    _temp_config = copy.deepcopy(_config)


def save_config():
    global _config, _temp_config
    _config = _temp_config
    with open(CONFIG_PATH, 'w') as f:
        json.dump(_config, f)


def get_output_format():
    return _config["output_format"]


def set_output_format(val):
    global _temp_config
    _temp_config["output_format"] = val


def get_output_folder():
    return _config["output_folder"]


def output_folder_exists():
    return os.path.exists(get_output_folder())


def set_output_folder(val):
    global _temp_config
    _temp_config["output_folder"] = val


def get_duplicity_mode():
    return _config["duplicity_mode"]


def set_duplicity_mode(val):
    global _temp_config
    _temp_config["duplicity_mode"] = val


def get_nn_loading():
    return _config["nn_loading"]


def set_nn_loading(val):
    global _temp_config
    _temp_config["nn_loading"] = val
