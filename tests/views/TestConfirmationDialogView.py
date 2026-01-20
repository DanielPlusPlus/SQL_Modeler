import unittest
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

from app.views.ConfirmationDialogView import ConfirmationDialogView

app = QApplication.instance() or QApplication([])


class TestConfirmationDialogView(unittest.TestCase):
    def setUp(self):
        self.dialog = ConfirmationDialogView(None, "Test Title", "Test text")

    def testDisplayDialogYesReturnsTrue(self):
        def clickYes():
            self.dialog.done(QMessageBox.StandardButton.Yes)

        QTimer.singleShot(0, clickYes)
        result = self.dialog.displayDialog()
        self.assertTrue(result)

    def testDisplayDialogNoReturnsFalse(self):
        def clickNo():
            self.dialog.done(QMessageBox.StandardButton.No)

        QTimer.singleShot(0, clickNo)
        result = self.dialog.displayDialog()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
