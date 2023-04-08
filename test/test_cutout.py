import json
import os
import shutil
import unittest

from cv2 import cv2

import src.managers.config_manager as cm
import src.managers.data_manager as dm
import src.managers.hash_manager as hm

from test.datagen import save_canvas_and_imgs


class TestCutout(unittest.TestCase):

    config = None
    config_path = None
    output_folder = None
    imgs_folder = None
    folder = None

    def setUp(self):
        self.folder = "./temp"
        self.canvas = self.folder + "/canvas.jpg"
        self.imgs_folder = self.folder + "/imgs"
        self.output_folder = self.folder + "/output"
        self.config = {
            "language": "en",
            "output_format": 0,
            "output_folder": self.output_folder,
            "duplicity_mode": 1,
            "nn_loading": 0
        }
        self.config_path = "test_config.json"
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)
        cm.load_config(self.config_path)
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.imgs_folder, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.folder)
        os.remove(self.config_path)

    def test_cutout(self):
        cm.load_config(self.config_path)
        cm.set_temp_output_folder()
        save_canvas_and_imgs(self.canvas, self.imgs_folder, "nn_test_imgs")
        dm.add_file([self.canvas])
        dm.process_next_image()
        dm.save_cutouts()
        out_imgs = [cv2.imread(f"{cm.get_temp_output_folder()}/{i}") for i in os.listdir(cm.get_temp_output_folder())]
        inp_imgs = [cv2.imread(f"{self.imgs_folder}/{i}") for i in os.listdir(self.imgs_folder)]
        out_hashes = []
        n = len(inp_imgs)
        for i in out_imgs:
            out_hashes.append(hm._get_hash(i))
            for r in range(3):
                out_hashes.append(hm._get_hash(cv2.rotate(i, r)))
        inp_hashes = [hm._get_hash(i) for i in inp_imgs]
        results = []
        for i in inp_hashes:
            res = False
            for j in out_hashes:
                if hm._get_similarity(i, j) > 0.8:
                    res = True
            results.append(res)
        self.assertEqual(n, results.count(True))


if __name__ == '__main__':
    unittest.main()
