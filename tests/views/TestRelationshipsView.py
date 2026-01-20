import sys
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QRect, QPoint

from app.enums.RelationshipsEnum import RelationshipsEnum
from app.views.RelationshipsView import RelationshipsView


class DummyTable:
    def __init__(self, rect):
        self._rect = rect

    def getRectangle(self):
        return self._rect


class DummyRelationship:
    def __init__(self, firstRect, secondRect, relType):
        self.FirstTable = DummyTable(firstRect)
        self.SecondTable = DummyTable(secondRect)
        self.relationshipType = relType

    def getRelationshipType(self):
        return self.relationshipType


class DummyRelationshipsModel:
    def __init__(self, relationships):
        self._relationships = relationships

    def getRelationships(self):
        return self._relationships


class TestRelationshipsView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        self.parentWindow = QWidget()

        rect1 = QRect(10, 10, 100, 50)
        rect2 = QRect(200, 100, 80, 40)
        rel = DummyRelationship(rect1, rect2, RelationshipsEnum.REL_1_1)
        self.relationshipsModel = DummyRelationshipsModel([rel])

    @patch('app.views.RelationshipsView.QPainter')
    def testDrawRelationshipsCallsPainterMethods(self, mockPainterClass):
        mockPainter = mockPainterClass.return_value

        RelationshipsView(self.relationshipsModel, self.parentWindow)

        mockPainterClass.assert_called_with(self.parentWindow)
        self.assertTrue(mockPainter.setPen.called)
        self.assertTrue(mockPainter.setRenderHint.called)
        self.assertTrue(mockPainter.drawLine.called)
        self.assertTrue(mockPainter.end.called)

    @patch('app.views.RelationshipsView.QPainter')
    def testDrawRelationshipBeingDrawnCallsDrawLine(self, mockPainterClass):
        mockPainter = mockPainterClass.return_value

        rv = RelationshipsView(self.relationshipsModel, self.parentWindow)
        firstTable = self.relationshipsModel.getRelationships()[0].FirstTable
        cursorPos = QPoint(150, 150)

        rv.drawRelationshipBeingDrawn(firstTable, cursorPos)

        mockPainter.setPen.assert_called()
        mockPainter.setRenderHint.assert_called()
        mockPainter.drawLine.assert_called()
        mockPainter.end.assert_called()


if __name__ == '__main__':
    unittest.main()