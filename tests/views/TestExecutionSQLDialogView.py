import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QTextEdit, QPushButton, QDialog
from PySide6.QtGui import QFont

from app.views.ExecutionSQLDialogView import ExecutionSQLDialogView

app = QApplication.instance() or QApplication([])


class TestExecutionSQLDialogView(unittest.TestCase):
    def setUp(self):
        self.testResult = "SELECT executed successfully."
        self.dialog = ExecutionSQLDialogView(None)
        self.dialog.setupUI(self.testResult)

    def testDialogComponentsExist(self):
        textEdit = self.dialog._ExecutionSQLDialogView__ExecutionResultTextEdit
        self.assertIsNotNone(textEdit)
        self.assertIsInstance(textEdit, QTextEdit)

        self.assertIsNotNone(self.dialog.okButton)
        self.assertIsInstance(self.dialog.okButton, QPushButton)

        self.assertIsNotNone(self.dialog.cancelButton)
        self.assertIsInstance(self.dialog.cancelButton, QPushButton)

    def testTextEditContentAndProperties(self):
        textEdit = self.dialog._ExecutionSQLDialogView__ExecutionResultTextEdit
        self.assertEqual(textEdit.toPlainText(), self.testResult)
        self.assertTrue(textEdit.isReadOnly())

        font: QFont = textEdit.font()
        self.assertEqual(font.family(), "Courier")
        self.assertEqual(font.pointSize(), 10)

    @patch.object(ExecutionSQLDialogView, 'exec', return_value=QDialog.Accepted)
    def testDisplayDialogReturnsTrueWhenOkClicked(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertEqual(result, QDialog.Accepted)
        mockExec.assert_called_once()

    @patch.object(ExecutionSQLDialogView, 'exec', return_value=QDialog.Rejected)
    def testDisplayDialogReturnsFalseWhenCancelClicked(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertEqual(result, QDialog.Rejected)
        mockExec.assert_called_once()


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)