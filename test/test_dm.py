import unittest
import os
import shutil
import cv2
import numpy as np

import src.managers.data_manager as dm
import src.managers.config_manager as cm


class TestDataManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_image = "./testingImages/output.jpg"
        cls.test_output_folder = "./output"
        cm.load_config()
        os.makedirs(cls.test_output_folder, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_output_folder)

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
        dm.process_next_image()
        cm.set_temp_output_folder()
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
