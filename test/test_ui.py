import sys
import unittest

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

from src.controllers.drop.drop_controller import DropUi
from src.controllers.main.main_controller import MainUi
import src.managers.config_manager as Cm


class MyTestCase(unittest.TestCase):
    app = QtWidgets.QApplication(sys.argv)
    sw = QWidget()
    sw.setWindowTitle("PicScan beta")
    Cm.load_config()
    main = MainUi(sw)
    drop = DropUi(sw)

    def test_center(self):
        center = self.main.center.isVisible()
        self.assertEqual(center, False)
        self.assertEqual(self.main.center.objectName(), "outer")
        self.assertEqual(self.main.center.layout(), self.main.main_h_layout)

    def test_layoutContainsWidgets(self):
        layout = self.drop.layout.layout()
        count = self.drop.layout.count()
        self.assertEqual(count, 6)
        for i in [self.drop.label_1, self.drop.label_2, self.drop.browser_button]:
            self.drop.layout.removeWidget(i)
        countUpdate = self.drop.layout.count()
        self.assertEqual(countUpdate, 3)

    def test_browseButtonConfigDropUi(self):
        button = self.drop.browser_button.text()
        self.assertEqual(self.drop.browser_button.isVisible(), False)
        self.assertEqual(self.drop.browser_button.objectName(), "browserButton")

    # def test_getDistance(self, number, number1):
    #     number[0] = 5.5
    #     number1[0] = 6.7
    #     result = graphicOperations._get_distance(int)(number[0], number1[0])
    #     self.assertEqual(result, 0.51313443543513513513)
    #
    # def test_editBrowseButton(self):
    #     edit = EditUi(self.sw, 1, self.main.fileNameLabel, self.main.canvas)

    def test_isImage(self):
        file_name = "test.jpg"
        file_name = file_name[file_name.rfind(".") + 1:]
        global bool
        if file_name in ["bmp", "jpeg", "jpg", "tiff", "png"]:
            bool = True
        else:
            bool = False
        self.assertEqual(bool, True)

    def test_isEmpty(self):
        global files

    # def test_buildButtonEdit(self):
    #     parent = self.main.scrollArea
    #     label = Label(parent, img, idx)
    #     frame = QFrame()


if __name__ == '__main__':
    unittest.main()
