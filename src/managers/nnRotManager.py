import numpy as np
import tensorflow as tf
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
import albumentations as A

from definitions import MODEL_PATH
import cv2

_model = None


def _augment(img):
    t = A.Compose(
        [
            A.Normalize(mean=0.0, std=1.0)
        ]
    )
    return t(image=img)["image"]


def _load_model():
    global _model
    _model = tf.keras.models.load_model(MODEL_PATH)
    print("LOADED")


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


def get_predictions(imgs):
    if _model is None:
        raise Exception("Model not loaded yet.")
    temp_imgs = []
    for img in imgs:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        img = cv2.resize(img, (128, 128))
        temp_imgs.append(img)
    gens, _ = gen_full(temp_imgs)
    augs = [_augment(x) for x in gens]
    preds = _model.predict(x=np.array(augs))
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
    is_loaded = pyqtSignal()

    def run_thread(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(lambda: self.ee())
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def ee(self):
        self.is_loaded.emit()


class Worker(QObject):
    finished = pyqtSignal()

    def run(self):
        _load_model()
        self.finished.emit()
