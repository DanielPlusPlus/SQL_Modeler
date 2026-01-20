import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox

from app.views.ErrorDialogView import ErrorDialogView

app = QApplication([])


class TestErrorDialogView(unittest.TestCase):
    def setUp(self):
        self.title = "Błąd"
        self.message = "Coś poszło nie tak"
        self.dialog = ErrorDialogView(None, self.title, self.message)

    def testDialogInitialization(self):
        self.assertEqual(self.dialog.windowTitle(), self.title)
        self.assertEqual(self.dialog.text(), self.message)
        self.assertEqual(self.dialog.icon(), QMessageBox.Icon.Critical)
        self.assertEqual(self.dialog.standardButtons(), QMessageBox.StandardButton.Ok)
        self.assertEqual(self.dialog.defaultButton().text(), "OK")

    @patch.object(ErrorDialogView, 'exec', return_value=QMessageBox.StandardButton.Ok)
    def testDisplayDialogReturnsTrueWhenOkClicked(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertTrue(result)
        mockExec.assert_called_once()

    @patch.object(ErrorDialogView, 'exec', return_value=QMessageBox.StandardButton.Cancel)
    def testDisplayDialogReturnsFalseWhenOtherButton(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertFalse(result)
        mockExec.assert_called_once()


if __name__ == "__main__":
    unittest.main()
