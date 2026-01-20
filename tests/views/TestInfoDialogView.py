import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox

from app.views.InfoDialogView import InfoDialogView

app = QApplication([])


class TestInfoDialogView(unittest.TestCase):
    def setUp(self):
        self.title = "Test Title"
        self.text = "This is an information message."
        self.dialog = InfoDialogView(None, self.title, self.text)

    def testDialogProperties(self):
        self.assertEqual(self.dialog.windowTitle(), self.title)
        self.assertEqual(self.dialog.text(), self.text)
        self.assertEqual(self.dialog.icon(), QMessageBox.Icon.Information)
        self.assertEqual(
            self.dialog.standardButtons(),
            QMessageBox.StandardButton.Ok
        )
        self.assertEqual(
            self.dialog.defaultButton().text(),
            self.dialog.button(QMessageBox.StandardButton.Ok).text()
        )

    @patch.object(InfoDialogView, 'exec', return_value=QMessageBox.StandardButton.Ok)
    def testDisplayDialogReturnsTrueOnOk(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertTrue(result)
        mockExec.assert_called_once()

    @patch.object(InfoDialogView, 'exec', return_value=QMessageBox.StandardButton.Cancel)
    def testDisplayDialogReturnsFalseOnCancel(self, mockExec):
        result = self.dialog.displayDialog()
        self.assertFalse(result)
        mockExec.assert_called_once()


if __name__ == "__main__":
    unittest.main()
