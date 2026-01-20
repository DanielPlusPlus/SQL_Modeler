import unittest

from PySide6.QtGui import QMouseEvent, QPaintEvent
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QApplication
from unittest.mock import MagicMock

from app.views.DrawingAreaView import DrawingAreaView

app = QApplication.instance() or QApplication([])


class TestDrawingAreaView(unittest.TestCase):
    def setUp(self):
        self.mockController = MagicMock()
        self.view = DrawingAreaView(self.mockController)

    def testSetTablesModelSetsModel(self):
        mockModel = MagicMock()
        self.view.setTablesModel(mockModel)
        self.assertEqual(self.view._DrawingAreaView__TablesModel, mockModel)

    def testMouseMoveEventCallsHandleMouseMoveAndUpdate(self):
        pos = QPointF(self.view.rect().center())
        event = QMouseEvent(
            QMouseEvent.Type.MouseMove, pos, pos, pos,
            Qt.NoButton, Qt.NoButton, Qt.NoModifier
        )
        self.view.update = MagicMock()
        self.view.mouseMoveEvent(event)
        self.mockController.handleMouseMove.assert_called_once_with(event)
        self.view.update.assert_called_once()

    def testMousePressEventCallsHandleMousePressAndUpdate(self):
        pos = QPointF(self.view.rect().center())
        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress, pos, pos, pos,
            Qt.LeftButton, Qt.LeftButton, Qt.NoModifier
        )
        self.view.update = MagicMock()
        self.view.mousePressEvent(event)
        self.mockController.handleMousePress.assert_called_once_with(event)
        self.view.update.assert_called_once()

    def testPaintEventCallsHandlePaintEvent(self):
        event = QPaintEvent(self.view.rect())
        self.view.paintEvent(event)
        self.mockController.handlePaintEvent.assert_called_once()

    def testSetupUISetsObjectName(self):
        self.view.setupUI()
        self.assertEqual(self.view.objectName(), "DrawingArea")


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)