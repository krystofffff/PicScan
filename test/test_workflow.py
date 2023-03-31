import json
import os
import shutil
import unittest

from cv2 import cv2

import src.managers.config_manager as cm
import src.managers.data_manager as dm
import src.managers.hash_manager as hm

from datagen import save_canvas_and_imgs


class TestWorkflow(unittest.TestCase):

    config = None
    config_path = None
    output_folder = None
    imgs_folder = None
    folder = None

    @classmethod
    def setUpClass(cls):
        cls.folder = "./temp"
        cls.canvas = cls.folder + "/canvas.jpg"
        cls.imgs_folder = cls.folder + "/imgs"
        cls.output_folder = cls.folder + "/output"
        cls.config = {
            "language": "en",
            "output_format": 0,
            "output_folder": cls.output_folder,
            "duplicity_mode": 1,
            "nn_loading": 0
        }
        cls.config_path = "test_config.json"
        with open(cls.config_path, 'w') as f:
            json.dump(cls.config, f)
        cm.load_config(cls.config_path)
        os.makedirs(cls.output_folder, exist_ok=True)
        os.makedirs(cls.imgs_folder, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.folder)
        os.remove(cls.config_path)

    def test_workflow(self):
        save_canvas_and_imgs(self.canvas, self.imgs_folder)
        dm.add_file([self.canvas])
        dm.process_next_image()
        dm.save_cutouts()
        out_imgs = [cv2.imread(f"{cm.get_temp_output_folder()}/{i}") for i in os.listdir(cm.get_temp_output_folder())]
        inp_imgs = [cv2.imread(f"{self.imgs_folder}/{i}") for i in os.listdir(self.imgs_folder)]
        out_hashes = []
        for i in out_imgs:
            out_hashes.append(hm._get_hash(i))
            for r in range(3):
                out_hashes.append(hm._get_hash(cv2.rotate(i, r)))
        inp_hashes = [hm._get_hash(i) for i in inp_imgs]
        results = []
        for i in inp_hashes:
            res = False
            for j in out_hashes:
                if hm._get_similarity(i, j) > 0.85:
                    res = True
            results.append(res)
        self.assertEqual(5, results.count(True))


if __name__ == '__main__':
    unittest.main()
