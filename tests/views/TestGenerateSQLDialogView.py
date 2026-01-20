import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QPushButton

from app.views.GenerateSQLDialogView import GenerateSQLDialogView
from app.views.widgets.CodeEditor import CodeEditor

app = QApplication([])


class TestGenerateSQLDialogView(unittest.TestCase):
    def setUp(self):
        self.testSql = "SELECT * FROM users;"
        self.dialog = GenerateSQLDialogView(None)
        self.dialog.setupUI(self.testSql)

    def testComponentsExist(self):
        self.assertIsInstance(self.dialog.SQLCodeTextEdit, CodeEditor)
        self.assertIsInstance(self.dialog.copyCodeButton, QPushButton)
        self.assertIsInstance(self.dialog.saveCodeButton, QPushButton)
        self.assertIsInstance(self.dialog.testCodeButton, QPushButton)
        self.assertIsInstance(self.dialog.okButton, QPushButton)
        self.assertIsInstance(self.dialog.cancelButton, QPushButton)

    def testCodeEditorProperties(self):
        codeEditor = self.dialog.SQLCodeTextEdit
        self.assertTrue(codeEditor.isReadOnly())
        self.assertEqual(codeEditor.toPlainText(), self.testSql)

    @patch.object(GenerateSQLDialogView, 'exec', return_value=GenerateSQLDialogView.Accepted)
    def testDisplayDialogReturnsTrueOnOk(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertTrue(result)
        mockExec.assert_called_once()

    @patch.object(GenerateSQLDialogView, 'exec', return_value=GenerateSQLDialogView.Rejected)
    def testDisplayDialogReturnsFalseOnCancel(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertFalse(result)
        mockExec.assert_called_once()


if __name__ == "__main__":
    unittest.main()
