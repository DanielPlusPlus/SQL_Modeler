import unittest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import QPoint, QRect

from app.views.TablesView import TablesView


class DummyTable:
    def __init__(self):
        self.getLeft = MagicMock(return_value=10)
        self.getTop = MagicMock(return_value=20)
        self.getTableWidth = MagicMock(return_value=100)
        self.getRowHeight = MagicMock(return_value=15)
        self.getRowsNumber = MagicMock(return_value=3)
        self.getTableName = MagicMock(return_value="TestTable")
        self.getTableColumns = MagicMock(return_value=[
            {"columnName": "col1"},
            {"columnName": "col2"},
            {"columnName": "col3"},
        ])
        self.getRectangle = MagicMock(return_value=QRect(10, 20, 100, 45))
        self.getTitleRectangle = MagicMock(return_value=QRect(10, 5, 100, 15))
        self.getTableCollapseStatus = MagicMock(return_value=False)


class DummyTablesModel:
    def getTables(self):
        return [DummyTable()]


class DummyParentWindow:
    pass


class TestTablesView(unittest.TestCase):
    @patch("app.views.TablesView.QPainter")
    def testDrawTablesCallsDrawTableForEachTable(self, mockQpainterClass):
        mockPainterInstance = MagicMock()
        mockQpainterClass.return_value = mockPainterInstance

        tablesModel = DummyTablesModel()
        parent = DummyParentWindow()
        view = TablesView(tablesModel, parent)

        mockQpainterClass.assert_called_with(parent)
        mockPainterInstance.setPen.assert_called()

        self.assertTrue(mockPainterInstance.drawText.called)
        self.assertTrue(mockPainterInstance.drawRect.called)

    @patch("app.views.TablesView.QPainter")
    def testDrawTempTableCreatesTableAndDrawsIt(self, mockQpainterClass):
        mockPainterInstance = MagicMock()
        mockQpainterClass.return_value = mockPainterInstance

        tablesModel = DummyTablesModel()
        parent = DummyParentWindow()
        view = TablesView(tablesModel, parent)

        position = QPoint(50, 50)
        view.drawTempTable(position, width=120, rowsHeight=25, rowsNumber=4)

        mockQpainterClass.assert_called_with(parent)
        mockPainterInstance.setPen.assert_called()
        self.assertTrue(mockPainterInstance.drawText.called)
        self.assertTrue(mockPainterInstance.drawRect.called)

    @patch("app.views.TablesView.QFont")
    def testDrawTableSetsFontBold(self, mockQfontClass):
        mockFontInstance = MagicMock()
        mockQfontClass.return_value = mockFontInstance

        mockPainter = MagicMock()
        dummyTable = DummyTable()

        tablesView = TablesView.__new__(TablesView)
        tablesView._TablesView__TablesModel = None
        tablesView._TablesView__ParentWindow = None

        tablesView._TablesView__drawTable(mockPainter, dummyTable)

        mockQfontClass.assert_called_with("Sans", 10)
        mockFontInstance.setBold.assert_called_with(True)
        mockPainter.setFont.assert_called_with(mockFontInstance)


if __name__ == "__main__":
    unittest.main()
