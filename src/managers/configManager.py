import json
import copy

from definitions import CONFIG_PATH

_config = {}
_temp_config = {}


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


def set_output_folder(val):
    global _temp_config
    _temp_config["output_folder"] = val


def get_similarity_mode():
    return _config["similarity_mode"]


def set_similarity_mode(val):
    global _temp_config
    _temp_config["similarity_mode"] = val
