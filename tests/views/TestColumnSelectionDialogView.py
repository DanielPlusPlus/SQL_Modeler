import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from app.views.ColumnSelectionDialogView import ColumnSelectionDialogView


app = QApplication.instance() or QApplication([])


class TestColumnSelectionDialogView(unittest.TestCase):
    def setUp(self):
        self.columns = [
            {"columnName": "id"},
            {"columnName": "name"},
            {"columnName": "email"},
        ]
        self.dialog = ColumnSelectionDialogView(None, self.columns)

    def testComboBoxItems(self):
        combo = self.dialog._ColumnSelectionDialogView__combo_box
        self.assertEqual(combo.count(), len(self.columns))
        for i, column in enumerate(self.columns):
            self.assertEqual(combo.itemText(i), column["columnName"])

    def testDisplayDialogAcceptedReturnsSelected(self):
        combo = self.dialog._ColumnSelectionDialogView__combo_box
        combo.setCurrentIndex(1)

        def acceptLater():
            QTimer.singleShot(100, self.dialog.accept)

        QTimer.singleShot(0, acceptLater)
        selected = self.dialog.displayDialog()
        self.assertEqual(selected, "name")

    def testDisplayDialogRejectedReturnsNone(self):
        def rejectLater():
            QTimer.singleShot(100, self.dialog.reject)

        QTimer.singleShot(0, rejectLater)
        selected = self.dialog.displayDialog()
        self.assertIsNone(selected)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
