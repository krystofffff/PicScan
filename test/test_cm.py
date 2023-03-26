import unittest
import json
from datetime import datetime
import os
import shutil
from unittest.mock import patch

import src.managers.config_manager as cm


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary folder to use for output
        self.output_folder = f"./test_output_folder"
        os.makedirs(self.output_folder)

        # Create a temporary config file to use for testing
        self.config = {
            "language": "en",
            "output_format": "png",
            "output_folder": self.output_folder,
            "duplicity_mode": 1,
            "nn_loading": 1
        }
        self.config_path = "test_config.json"
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)

    def tearDown(self):
        # Delete the temporary output folder and config file
        shutil.rmtree(self.output_folder)
        os.remove(self.config_path)

    def test_load_config(self):
        # Test that load_config() loads the config file correctly
        cm.load_config(path=self.config_path)
        self.assertEqual(cm.get_language(), self.config["language"])
        self.assertEqual(cm.get_output_format(), self.config["output_format"])
        self.assertEqual(cm.get_output_folder(), self.config["output_folder"])
        self.assertEqual(cm.get_duplicity_mode(), self.config["duplicity_mode"])
        self.assertEqual(cm.get_nn_loading(), self.config["nn_loading"])

    def test_set_language(self):
        # Test that set_language() sets the language correctly in the temporary config
        cm.create_temp_config()
        cm.set_language("en")
        self.assertEqual(cm._temp_config["language"], "en")

    def test_get_language(self):
        # Test that get_language() returns the correct language from the config
        cm.load_config(path=self.config_path)
        self.assertEqual(cm.get_language(), self.config["language"])

    def test_set_temp_output_folder(self):
        # Test that set_temp_output_folder() sets the _temp_output_folder variable correctly
        cm.create_temp_config()
        cm.set_temp_output_folder()
        now = datetime.now()
        t = now.strftime("%Y-%m-%d-%H-%M-%S")
        expected_temp_output_folder = f"{self.config['output_folder']}/{t}"
        self.assertEqual(cm.get_temp_output_folder(), expected_temp_output_folder)

    def test_clear_temp_output_folder(self):
        # Test that clear_temp_output_folder() clears the _temp_output_folder variable
        cm.load_config(path=self.config_path)
        cm.create_temp_config()
        cm.set_temp_output_folder()
        cm.clear_temp_output_folder()
        self.assertIsNone(cm._temp_output_folder)

    def test_save_config(self):
        # Test that save_config() saves the temporary config to the config file
        cm.create_temp_config()
        cm.set_language("fr")
        cm.save_config(path=self.config_path)
        with open(self.config_path, 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config["language"], "fr")

    def test_output_folder_exists(self):
        # Test that output_folder_exists() returns True when the output folder exists and False otherwise
        cm.load_config(path=self.config_path)
        self.assertTrue(cm.output_folder_exists())

    def test_set_output_folder(self):
        #    def test_set_output_folder(self):
        # Test that set_output_folder() sets the output folder correctly in the temporary config
        cm.create_temp_config()
        cm.set_output_folder("new_output_folder")
        self.assertEqual(cm._temp_config["output_folder"], "new_output_folder")

    def test_get_duplicity_mode(self):
        # Test that get_duplicity_mode() returns the correct duplicity mode from the config
        cm.load_config(path=self.config_path)
        self.assertEqual(cm.get_duplicity_mode(), self.config["duplicity_mode"])

    def test_set_duplicity_mode(self):
        # Test that set_duplicity_mode() sets the duplicity mode correctly in the temporary config
        cm.create_temp_config()
        cm.set_duplicity_mode("overwrite")
        self.assertEqual(cm._temp_config["duplicity_mode"], "overwrite")

    def test_get_nn_loading(self):
        # Test that get_nn_loading() returns the correct NN loading option from the config
        cm.load_config(path=self.config_path)
        self.assertEqual(cm.get_nn_loading(), self.config["nn_loading"])

    def test_set_nn_loading(self):
        # Test that set_nn_loading() sets the NN loading option correctly in the temporary config
        cm.create_temp_config()
        cm.set_nn_loading("pretrained")
        self.assertEqual(cm._temp_config["nn_loading"], "pretrained")


if __name__ == '__main__':
    unittest.main()
