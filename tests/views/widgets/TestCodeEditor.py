import sys
import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QPaintEvent, QResizeEvent

from app.views.widgets.CodeEditor import CodeEditor
from app.views.widgets.LineNumberArea import LineNumberArea

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


class TestCodeEditor(unittest.TestCase):
    def setUp(self):
        self.editor = CodeEditor()

    def testInitialFont(self):
        font = self.editor.font()
        self.assertEqual(font.family(), "Courier")
        self.assertEqual(font.pointSize(), 10)

    def testLineNumberAreaCreated(self):
        self.assertIsInstance(self.editor._CodeEditor__line_number_area, LineNumberArea)

    def testLineNumberAreaWidth(self):
        width = self.editor.line_number_area_width()
        self.assertIsInstance(width, int)
        self.assertGreater(width, 0)

    def testUpdateLineNumberAreaWidthSetsMargins(self):
        self.editor._CodeEditor__update_line_number_area_width(0)
        margins = self.editor.viewportMargins()
        self.assertGreater(margins.left(), 0)

    def testUpdateLineNumberAreaScrollsOrUpdates(self):
        class DummyRect:
            def __init__(self):
                self._contains = False

            def contains(self, other):
                return self._contains

            def y(self):
                return 0

            def height(self):
                return 10

            def bottom(self):
                return 10

        rect = DummyRect()

        self.editor._CodeEditor__update_line_number_area(rect, 5)

        self.editor._CodeEditor__update_line_number_area(rect, 0)

        rect._contains = True
        self.editor._CodeEditor__update_line_number_area(rect, 0)

    def testResizeEventSetsGeometry(self):
        oldSize = QSize(100, 100)
        newSize = QSize(200, 200)
        event = QResizeEvent(newSize, oldSize)
        self.editor.resizeEvent(event)
        self.assertIsNotNone(self.editor._CodeEditor__line_number_area.geometry())

    def testLineNumberAreaPaintEventRuns(self):
        rect = QRect(0, 0, 50, 50)
        event = QPaintEvent(rect)
        self.editor.line_number_area_paint_event(event)

    def testHighlightCurrentLineAddsSelection(self):
        self.editor.setReadOnly(False)
        self.editor._CodeEditor__highlight_current_line()
        selections = self.editor.extraSelections()
        self.assertGreater(len(selections), 0)

    def testHighlightCurrentLineNoSelectionIfReadonly(self):
        self.editor.setReadOnly(True)
        self.editor._CodeEditor__highlight_current_line()
        selections = self.editor.extraSelections()
        self.assertEqual(len(selections), 0)


if __name__ == "__main__":
    unittest.main()