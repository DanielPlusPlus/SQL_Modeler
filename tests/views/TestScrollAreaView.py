import unittest
from PySide6.QtWidgets import QApplication, QWidget

from app.views.ScrollAreaView import ScrollAreaView

import sys

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


class TestScrollAreaView(unittest.TestCase):
    def setUp(self):
        self.parent = QWidget()

    def testConstructor(self):
        scrollArea = ScrollAreaView(self.parent)
        self.assertIsInstance(scrollArea, ScrollAreaView)

    def testSetupUISetsWidgetAndResizable(self):
        scrollArea = ScrollAreaView(self.parent)
        drawingArea = QWidget()

        scrollArea.setupUI(drawingArea)

        self.assertEqual(scrollArea.widget(), drawingArea)
        self.assertTrue(scrollArea.widgetResizable())


if __name__ == "__main__":
    unittest.main()
