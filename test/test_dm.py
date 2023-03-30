import json
import os
import shutil
import unittest

import numpy as np

import src.managers.config_manager as cm
import src.managers.data_manager as dm


class TestDataManager(unittest.TestCase):

    config = None
    config_path = None
    test_output_folder = None

    @classmethod
    def setUpClass(cls):
        cls.test_image = "./testingImages/output.jpg"
        cls.test_output_folder = "./output"
        cls.config = {
            "language": "en",
            "output_format": 0,
            "output_folder": cls.test_output_folder,
            "duplicity_mode": 1,
            "nn_loading": 0
        }
        cls.config_path = "test_config.json"
        with open(cls.config_path, 'w') as f:
            json.dump(cls.config, f)
        cm.load_config(cls.config_path)
        os.makedirs(cls.test_output_folder, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_output_folder)
        os.remove(cls.config_path)

    def setUp(self):
        dm.clear_data()

    def test_add_file(self):
        dm.set_file_count([self.test_image])
        self.assertEqual(dm.get_file_count(), 1)
        dm.add_file([self.test_image])
        self.assertFalse(dm.is_empty())

    def test_process_next_image(self):
        dm.add_file([self.test_image])
        dm.process_next_image()
        self.assertIsNotNone(dm.get_canvas())

    def test_save_cutouts(self):
        dm.add_file([self.test_image])
        cm.clear_temp_output_folder()
        cm.set_temp_output_folder()
        dm.process_next_image()
        dm.save_cutouts()
        saved_files = os.listdir(cm.get_temp_output_folder())
        self.assertNotEqual(len(saved_files), 0)

    def test_rotate_cutout(self):
        dm.add_file([self.test_image])
        dm.process_next_image()
        dm.generate_cutouts()
        cutouts = dm.get_cutouts()
        if len(cutouts) > 0:
            original_img = cutouts[0].img.copy()
            dm.rotate_cutout(0)
            rotated_img = cutouts[0].img
            self.assertFalse(np.array_equal(original_img, rotated_img))

    def test_toggle_cutout(self):
        dm.add_file([self.test_image])
        dm.process_next_image()
        dm.generate_cutouts()
        cutouts = dm.get_cutouts()
        if len(cutouts) > 0:
            original_state = cutouts[0].enabled
            dm.toggle_cutout(0)
            toggled_state = cutouts[0].enabled
            self.assertNotEqual(original_state, toggled_state)


if __name__ == '__main__':
    unittest.main()
