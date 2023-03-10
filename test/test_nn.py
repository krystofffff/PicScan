import os
import unittest

import cv2
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtTest import QTest

from src.managers import nnRotManager as Nm
from src.managers.nnRotManager import Loader


class MyClass(QObject):
    my_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        QTimer.singleShot(1000, self.my_signal.emit)


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.imgs = []
        dir = "nn_test_imgs"
        for file in os.listdir(dir):
            i = cv2.imread(dir + "/" + file)
            self.imgs.append(i)

    def test_not_loaded(self):
        self.assertRaises(Exception, lambda x: Nm.get_predictions(self.imgs))

    def test_model_predictions(self):
        loader = Loader()
        loader.run_thread()
        QTest.qWait(10_000)
        x, y = Nm.gen_full(self.imgs)
        preds = Nm.get_predictions(x)
        counter = 0
        for idx, i in enumerate(preds):
            if i == y[idx]:
                counter += 1
        counter /= len(preds)
        self.assertTrue(counter > 0.9)
