import unittest
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QAction

from app.views.RelationshipContextMenuView import RelationshipContextMenuView


class TestRelationshipContextMenuView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        self.parent = QWidget()
        self.menu = RelationshipContextMenuView(self.parent)
        self.menu.setupUI()

    def testActionsCreated(self):
        self.assertIsInstance(self.menu.actionDeleteRelationship, QAction)
        self.assertEqual(self.menu.actionDeleteRelationship.text(), "Delete Relationship")

    def testActionsAddedToMenu(self):
        actions = self.menu.actions()
        texts = [action.text() for action in actions]
        self.assertIn("Delete Relationship", texts)


if __name__ == "__main__":
    unittest.main()
