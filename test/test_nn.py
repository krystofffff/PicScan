import os

import cv2
from src.managers import nn_rot_manager as nm
from src.managers.nn_rot_manager import Loader


class TestNN:
    imgs = []

    def setup_method(self):
        fld = "nn_test_imgs"
        for file in os.listdir(fld):
            i = cv2.imread(fld + "/" + file)
            self.imgs.append(i)

    def test_not_loaded(self):
        try:
            nm.get_predictions(self.imgs)
            assert False
        except nm.NNNotLoadedException:
            assert True

    def test_model_predictions(self, qtbot):
        loader = Loader()
        with qtbot.waitSignal(loader.is_loaded, timeout=15_000):
            loader.run_thread()
        x, y = nm.gen_full(self.imgs)
        preds = nm.get_predictions(x)
        counter = 0
        for idx, i in enumerate(preds):
            if i == y[idx]:
                counter += 1
        counter /= len(preds)
        assert counter > 0.9
