import unittest
from PySide6.QtWidgets import QApplication, QMenu

from app.views.InheritanceContextMenuView import InheritanceContextMenuView

app = QApplication([])


class TestInheritanceContextMenuView(unittest.TestCase):
    def setUp(self):
        self.menu = InheritanceContextMenuView(None)
        self.menu.setupUI()

    def testInheritance(self):
        self.assertIsInstance(self.menu, QMenu)

    def testActionsExist(self):
        self.assertTrue(hasattr(self.menu, 'actionDeleteInheritance'))

    def testActionsText(self):
        self.assertEqual(self.menu.actionDeleteInheritance.text(), "Delete Inheritance")

    def testActionsAreAddedToMenu(self):
        actions = self.menu.actions()
        self.assertIn(self.menu.actionDeleteInheritance, actions)


if __name__ == "__main__":
    unittest.main()
