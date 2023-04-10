import os

import cv2
import numpy as np
import tensorflow as tf
from PyQt5.QtCore import QObject, pyqtSignal, QThread

import src.utils.graphic_utils as gra
from definitions import MODEL_PATH

_model = None
model_is_loading = False


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


def is_model_loaded():
    return _model is not None


def load_model_async():
    global model_is_loading
    model_is_loading = True
    loader.run_thread()


def _load_model():
    global _model
    _model = tf.keras.models.load_model(MODEL_PATH)


def gen_full(imgs):
    x, y = [], []
    for img in imgs:
        for r in range(4):
            if not r == 3:
                r_image = cv2.rotate(img, r)
            else:
                r_image = img.copy()
            x.append(r_image)
            y.append(r)
    return x, y


def rot_list(li, n):
    return li[n:] + li[:n]


class NNNotLoadedException(Exception):
    pass


def get_predictions(imgs):
    if _model is None:
        raise NNNotLoadedException()
    temp_imgs = []
    for img in imgs:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        img = cv2.resize(img, (128, 128))
        temp_imgs.append(img)
    gens, _ = gen_full(temp_imgs)
    augs = [gra.augment(x) for x in gens]
    preds = _model.predict(x=np.array(augs), verbose=0)
    res = []
    for i in range(0, len(preds), 4):
        p = [0 for _ in range(4)]
        for j in range(4):
            c = rot_list(preds[i + j].tolist(), j + 1 % 4)
            p = [x + y for x, y in zip(c, p)]
        idx = np.argmax(p)
        res.append(idx)
    return res


class Loader(QObject):
    is_loaded = pyqtSignal(bool)

    def run_thread(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(lambda: self.finished())
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def finished(self):
        global model_is_loading
        model_is_loading = False
        self.is_loaded.emit(True)


class Worker(QObject):
    finished = pyqtSignal()

    def run(self):
        _load_model()
        self.finished.emit()


loader = Loader()
