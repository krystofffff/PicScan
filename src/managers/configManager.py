import json
import copy

_config = {}
_temp_config = {}


def load_config():
    global _config
    with open("src/config.json", 'r') as f:
        _config = json.load(f)


def create_temp_config():
    global _temp_config, _config
    _temp_config = copy.deepcopy(_config)


def save_config():
    global _config, _temp_config
    _config = _temp_config
    with open("src/config.json", 'w') as f:
        json.dump(_config, f)


def get_output_format():
    global _config
    return _config["output_format"]


def get_output_folder():
    global _config
    return _config["output_folder"]


def set_output_format(val):
    global _temp_config
    _temp_config["output_format"] = val


def set_output_folder(val):
    global _temp_config
    _temp_config["output_folder"] = val
