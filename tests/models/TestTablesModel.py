import unittest
from PySide6.QtCore import QPoint

from app.models.TablesModel import TablesModel
from app.models.TableModel import TableModel


class TestTablesModel(unittest.TestCase):
    def setUp(self):
        self.model = TablesModel()

    def testAddTableIncreasesListAndTableNumber(self):
        pos = QPoint(100, 100)
        self.model.addTable(pos)
        tables = self.model.getTables()
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0].getTableNumber(), 1)
        self.model.addTable(QPoint(200, 200))
        self.assertEqual(len(self.model.getTables()), 2)
        self.assertEqual(self.model.getTables()[1].getTableNumber(), 2)

    def testAddSelectedTableAppendsTable(self):
        table = TableModel(10, 20, 100, 20, 5, 99)
        self.model.addSelectedTable(table)
        self.assertIn(table, self.model.getTables())

    def testClearTablesEmptiesList(self):
        self.model.addTable(QPoint(0, 0))
        self.assertTrue(len(self.model.getTables()) > 0)
        self.model.clearTables()
        self.assertEqual(len(self.model.getTables()), 0)

    def testDeleteSelectedTableRemovesTable(self):
        table1 = TableModel(10, 20, 100, 20, 5, 1)
        table2 = TableModel(30, 40, 100, 20, 5, 2)
        self.model.addSelectedTable(table1)
        self.model.addSelectedTable(table2)
        self.model.deleteSelectedTable(table1)
        self.assertNotIn(table1, self.model.getTables())
        self.assertIn(table2, self.model.getTables())

    def testGetTableFromPositionReturnsCorrectTable(self):
        self.model.addTable(QPoint(100, 100))
        self.model.addTable(QPoint(300, 300))

        posInsideFirst = QPoint(100, 100)
        posInsideSecond = QPoint(300, 300)
        posOutside = QPoint(0, 0)

        table1 = self.model.getTableFromPosition(posInsideFirst)
        table2 = self.model.getTableFromPosition(posInsideSecond)
        noTable = self.model.getTableFromPosition(posOutside)

        self.assertIsNotNone(table1)
        self.assertIsNotNone(table2)
        self.assertNotEqual(table1, table2)
        self.assertIsNone(noTable)

    def testGetTableFromPositionWithEmptyTables(self):
        pos = QPoint(50, 50)
        self.assertIsNone(self.model.getTableFromPosition(pos))


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
