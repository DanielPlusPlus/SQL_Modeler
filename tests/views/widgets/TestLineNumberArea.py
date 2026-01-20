import unittest
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QSize
from PySide6.QtGui import QPaintEvent
import sys

from app.views.widgets.LineNumberArea import LineNumberArea


class DummyEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.paint_event_called_with = None

    def line_number_area_width(self):
        return 42

    def line_number_area_paint_event(self, event):
        self.paint_event_called_with = event


class TestLineNumberArea(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if not cls.app:
            cls.app = QApplication(sys.argv)

    def setUp(self):
        self.mockEditor = DummyEditor()
        self.lineNumberArea = LineNumberArea(self.mockEditor)

    def testSizeHintReturnsWidthFromEditor(self):
        size = self.lineNumberArea.sizeHint()
        self.assertIsInstance(size, QSize)
        self.assertEqual(size.width(), 42)
        self.assertEqual(size.height(), 0)

    def testPaintEventCallsEditorPaintEvent(self):
        event = QPaintEvent(self.lineNumberArea.rect())
        self.lineNumberArea.paintEvent(event)
        self.assertIs(self.mockEditor.paint_event_called_with, event)


if __name__ == "__main__":
    unittest.main()
