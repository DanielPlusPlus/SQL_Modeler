import unittest
from PySide6.QtCore import QPoint

from app.models.TableModel import TableModel
from app.models.TableColumnsModel import TableColumnsModel


class TestTableModel(unittest.TestCase):
    def setUp(self):
        self.x = 100
        self.y = 200
        self.width = 300
        self.rowHeight = 20
        self.minRowsNumber = 5
        self.tableNumber = 1
        self.table = TableModel(self.x, self.y, self.width, self.rowHeight, self.minRowsNumber, self.tableNumber)

    def testInitialRectangleAndProperties(self):
        rect = self.table.getRectangle()
        expectedX = self.x - self.width // 2
        expectedY = self.y - (self.rowHeight * self.minRowsNumber) // 2
        self.assertEqual(rect.x(), expectedX)
        self.assertEqual(rect.y(), expectedY)
        self.assertEqual(rect.width(), self.width)
        self.assertEqual(rect.height(), self.rowHeight * self.minRowsNumber)

        self.assertEqual(self.table.getTableWidth(), self.width)
        self.assertEqual(self.table.getRowHeight(), self.rowHeight)
        self.assertEqual(self.table.getRowsNumber(), self.minRowsNumber)
        self.assertEqual(self.table.getTableNumber(), self.tableNumber)
        self.assertEqual(self.table.getTableName(), "Table 1")

    def testTableNameWithoutNumber(self):
        table = TableModel(self.x, self.y, self.width, self.rowHeight, self.minRowsNumber, 0)
        self.assertEqual(table.getTableName(), "New Table")

    def testEditTableName(self):
        newName = "My Table"
        self.table.editTableName(newName)
        self.assertEqual(self.table.getTableName(), newName)

    def testGetTableColumnsModelAndColumns(self):
        self.assertIsInstance(self.table.getTableColumnsModel(), TableColumnsModel)
        self.assertEqual(self.table.getTableColumns(), [])

    def testChangeTableDimensions(self):
        dummyModel = TableColumnsModel(columns=[{
            "columnName": f"col{i}",
            "dataType": "INT",
            "length": 0,
            "unique": False,
            "notNull": False,
            "pk": False,
            "fk": False,
        } for i in range(10)])
        self.table.changeTableColumnsModel(dummyModel)
        self.table.changeTableDimensions()

        self.assertEqual(self.table.getRowsNumber(), 10)
        self.assertEqual(self.table.getRectangle().height(), 10 * self.rowHeight)

        dummyModel2 = TableColumnsModel(columns=[])
        self.table.changeTableColumnsModel(dummyModel2)
        self.table.changeTableDimensions()
        self.assertEqual(self.table.getRowsNumber(), self.minRowsNumber)

    def testChangeTablePosition(self):
        newX = 500
        newY = 600
        self.table.changeTablePosition(newX, newY)
        rect = self.table.getRectangle()
        expectedX = newX - self.width // 2
        expectedY = newY - (self.rowHeight * self.table.getRowsNumber()) // 2
        self.assertEqual(rect.x(), expectedX)
        self.assertEqual(rect.y(), expectedY)

    def testContainsPoint(self):
        rect = self.table.getRectangle()
        insidePoint = QPoint(rect.center().x(), rect.center().y())
        self.assertTrue(self.table.contains(insidePoint))

        outsidePoint = QPoint(rect.right() + 10, rect.bottom() + 10)
        self.assertFalse(self.table.contains(outsidePoint))


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)