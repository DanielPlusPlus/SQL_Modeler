import unittest
from PySide6.QtCore import Qt

from app.models.TableColumnsModel import TableColumnsModel


class TestTableColumnsModel(unittest.TestCase):
    def setUp(self):
        self.sampleColumns = [
            {
                "columnName": "id",
                "dataType": "INT",
                "length": 11,
                "unique": True,
                "notNull": True,
                "pk": True,
                "fk": False,
            },
            {
                "columnName": "name",
                "dataType": "VARCHAR",
                "length": 50,
                "unique": False,
                "notNull": False,
                "pk": False,
                "fk": False,
            },
        ]
        self.model = TableColumnsModel(self.sampleColumns)

    def testRowAndColumnCount(self):
        self.assertEqual(self.model.rowCount(), len(self.sampleColumns))
        self.assertEqual(self.model.columnCount(), 7)

    def testDataDisplayRole(self):
        index = self.model.index(0, 0)
        self.assertEqual(self.model.data(index, Qt.DisplayRole), "id")

        index = self.model.index(1, 1)
        self.assertEqual(self.model.data(index, Qt.DisplayRole), "VARCHAR")

        index = self.model.index(1, 2)
        self.assertEqual(self.model.data(index, Qt.DisplayRole), 50)

        indexEmpty = self.model.index(0, 3)
        self.assertEqual(self.model.data(indexEmpty, Qt.DisplayRole), "")

    def testDataCheckStateRole(self):
        index = self.model.index(0, 3)
        self.assertEqual(self.model.data(index, Qt.CheckStateRole), Qt.Checked)

        index = self.model.index(1, 3)
        self.assertEqual(self.model.data(index, Qt.CheckStateRole), Qt.Unchecked)

        indexPk = self.model.index(0, 5)
        self.assertEqual(self.model.data(indexPk, Qt.CheckStateRole), Qt.Checked)

        indexFk = self.model.index(1, 6)
        self.assertEqual(self.model.data(indexFk, Qt.CheckStateRole), Qt.Unchecked)

    def testFlags(self):
        self.model.isEditColumnsSelected = True

        for col in (0, 1, 2):
            flags = self.model.flags(self.model.index(0, col))
            self.assertTrue(flags & Qt.ItemIsSelectable)
            self.assertTrue(flags & Qt.ItemIsEnabled)
            self.assertTrue(flags & Qt.ItemIsEditable)

        for col in (3, 4, 5):
            flags = self.model.flags(self.model.index(0, col))
            self.assertTrue(flags & Qt.ItemIsSelectable)
            self.assertTrue(flags & Qt.ItemIsEnabled)
            self.assertTrue(flags & Qt.ItemIsUserCheckable)

        flags = self.model.flags(self.model.index(0, 6))
        self.assertTrue(flags & Qt.ItemIsSelectable)
        self.assertTrue(flags & Qt.ItemIsEnabled)
        self.assertFalse(flags & Qt.ItemIsUserCheckable)

    def testSetDataEditRole(self):
        index = self.model.index(1, 0)
        self.assertTrue(self.model.setData(index, "new_name", Qt.EditRole))
        self.assertEqual(self.model.data(index, Qt.DisplayRole), "new_name")

        index = self.model.index(1, 1)
        self.assertTrue(self.model.setData(index, "TEXT", Qt.EditRole))
        self.assertEqual(self.model.data(index, Qt.DisplayRole), "TEXT")

        index = self.model.index(1, 2)
        self.assertTrue(self.model.setData(index, 100, Qt.EditRole))
        self.assertEqual(self.model.data(index, Qt.DisplayRole), 100)

    def testSetDataCheckStateRole(self):
        index = self.model.index(1, 3)
        self.assertTrue(self.model.setData(index, Qt.Checked, Qt.CheckStateRole))
        self.assertTrue(self.model._TableColumnsModel__columns[1]["unique"])

        index = self.model.index(1, 4)
        self.assertTrue(self.model.setData(index, Qt.Checked, Qt.CheckStateRole))
        self.assertTrue(self.model._TableColumnsModel__columns[1]["notNull"])

        index = self.model.index(1, 5)
        self.assertTrue(self.model.setData(index, Qt.Checked, Qt.CheckStateRole))
        self.assertTrue(self.model._TableColumnsModel__columns[1]["pk"])

        index = self.model.index(1, 6)
        self.assertTrue(self.model.setData(index, Qt.Checked, Qt.CheckStateRole))
        self.assertTrue(self.model._TableColumnsModel__columns[1]["fk"])

    def testHeaderData(self):
        for i, header in enumerate(["Column Name", "Type", "Length", "UNIQUE", "NOT NULL", "PK", "FK"]):
            self.assertEqual(self.model.headerData(i, Qt.Horizontal, Qt.DisplayRole), header)
        self.assertEqual(self.model.headerData(0, Qt.Vertical, Qt.DisplayRole), "1")
        self.assertEqual(self.model.headerData(1, Qt.Vertical, Qt.DisplayRole), "2")

    def testAddAndDeleteColumn(self):
        oldCount = self.model.rowCount()

        self.model.addColumn("price", "FLOAT", 10)
        self.assertEqual(self.model.rowCount(), oldCount + 1)
        self.assertEqual(self.model._TableColumnsModel__columns[-1]["columnName"], "price")

        self.model.deleteColumn(oldCount)
        self.assertEqual(self.model.rowCount(), oldCount)

    def testSetForeignKeyByColumnName(self):
        self.assertFalse(self.model.setForeignKeyByColumnName("id"))
        self.assertTrue(self.model.setForeignKeyByColumnName("name"))
        self.assertTrue(self.model._TableColumnsModel__columns[1]["fk"])

        self.assertFalse(self.model.setForeignKeyByColumnName("nonexistent"))

    def testGetColumns(self):
        self.assertEqual(self.model.getColumns(), self.sampleColumns)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)