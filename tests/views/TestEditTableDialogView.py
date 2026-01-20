import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QStandardItemModel

from app.views.EditTableDialogView import EditTableDialogView

app = QApplication([])


class MockTable:
    def getTableName(self):
        return "MockTable"

    def getTableColumnsModel(self):
        model = QStandardItemModel()
        model.setColumnCount(3)
        model.setRowCount(2)
        return model


class TestEditTableDialogView(unittest.TestCase):
    def setUp(self):
        self.mockTable = MockTable()
        self.dialog = EditTableDialogView(None, self.mockTable)
        self.dialog.setupUi()

    def testUiComponentsExist(self):
        self.assertIsNotNone(self.dialog.tableNameLineEdit)
        self.assertIsNotNone(self.dialog.columnNameLineEdit)
        self.assertIsNotNone(self.dialog.dataTypeComboBox)
        self.assertIsNotNone(self.dialog.lengthSpinBox)
        self.assertIsNotNone(self.dialog.tableView)
        self.assertIsNotNone(self.dialog.addColumnButton)
        self.assertIsNotNone(self.dialog.deleteColumnButton)
        self.assertIsNotNone(self.dialog.editColumnButton)
        self.assertIsNotNone(self.dialog.cancelButton)
        self.assertIsNotNone(self.dialog.okButton)

    def testTableNameIsSetCorrectly(self):
        self.assertEqual(self.dialog.tableNameLineEdit.text(), "MockTable")

    def testDataTypesAreLoaded(self):
        expectedDataTypes = [
            "NUMBER", "FLOAT", "CHAR", "VARCHAR2", "NCHAR",
            "NVARCHAR2", "DATE", "CLOB", "BLOB"
        ]
        actualDataTypes = [self.dialog.dataTypeComboBox.itemText(i) for i in
                             range(self.dialog.dataTypeComboBox.count())]
        self.assertEqual(expectedDataTypes, actualDataTypes)


if __name__ == "__main__":
    unittest.main()
