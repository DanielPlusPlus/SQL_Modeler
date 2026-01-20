import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize

from app.views.ToolBarView import ToolBarView

app = QApplication.instance() or QApplication([])


class TestToolBarView(unittest.TestCase):
    def testSetupUI(self):
        toolbar = ToolBarView(None)
        toolbar.setupUI()

        self.assertEqual(toolbar.iconSize(), QSize(48, 48))
        actionsTexts = [action.text() for action in toolbar.actions()]

        expectedTexts = [
            "Create Table",
            "Create 1:1 Relationship",
            "Create 1:n Relationship",
            "Create n:n Relationship",
            "Create Inheritance Relationship",
            "Export Diagram",
            "Generate SQL Code",
        ]

        self.assertListEqual(actionsTexts, expectedTexts)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)