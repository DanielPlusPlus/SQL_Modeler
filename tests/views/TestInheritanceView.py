import sys
import unittest
from PySide6.QtWidgets import QApplication, QWidget
from unittest.mock import MagicMock, patch
from PySide6.QtCore import QRect, QPoint

from app.views.InheritancesView import InheritancesView

app = None


class TestInheritancesView(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global app
        if not QApplication.instance():
            app = QApplication(sys.argv)

    def setUp(self):
        self.mockModel = MagicMock()
        self.mockParentWindow = QWidget()
        self.view = InheritancesView(self.mockModel, self.mockParentWindow)

    def testEdgePointHorizontal(self):
        rect1 = QRect(0, 0, 100, 100)
        rect2 = QRect(200, 0, 100, 100)
        point = self.view.edgePoint(rect1, rect2)
        self.assertIsInstance(point, QPoint)

    def testDrawInheritanceBeingDrawnCallsDrawLine(self):
        mockTable = MagicMock()
        mockTable.getRectangle.return_value = QRect(0, 0, 100, 100)
        cursorPos = QPoint(150, 150)
        with patch("app.views.InheritancesView.QPainter") as mockPainterClass:
            mockPainterInstance = mockPainterClass.return_value
            self.view.drawInheritanceBeingDrawn(mockTable, cursorPos)
            mockPainterInstance.drawLine.assert_called()


if __name__ == "__main__":
    unittest.main()
