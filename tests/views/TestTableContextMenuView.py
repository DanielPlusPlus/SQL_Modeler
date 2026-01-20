import unittest
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QAction
import sys

from app.views.TableContextMenuView import TableContextMenuView

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


class TestTableContextMenuView(unittest.TestCase):
    def setUp(self):
        self.parent = QWidget()
        self.menu = TableContextMenuView(self.parent)

    def testConstructor(self):
        self.assertIsInstance(self.menu, TableContextMenuView)

    def testSetupUIAddsActions(self):
        self.menu.setupUI()

        actions = self.menu.actions()
        self.assertEqual(len(actions), 3)

        actionTexts = [action.text() for action in actions]
        self.assertIn("Collapse/Expand Table", actionTexts)
        self.assertIn("Edit Table", actionTexts)
        self.assertIn("Delete Table", actionTexts)

        for action in actions:
            self.assertIsInstance(action, QAction)


if __name__ == "__main__":
    unittest.main()