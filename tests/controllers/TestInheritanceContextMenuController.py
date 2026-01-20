import unittest
from unittest.mock import MagicMock

from app.controllers.InheritanceContextMenuController import InheritanceContextMenuController


class TestInheritanceContextMenuController(unittest.TestCase):
    def setUp(self):
        self.view = MagicMock()
        self.view.actionDeleteInheritance = MagicMock()
        self.view.actionDeleteInheritance.triggered.connect = MagicMock()

        self.controller = InheritanceContextMenuController(self.view)

    def testInitialStateIsUnselected(self):
        self.assertFalse(self.controller.getSelectDeleteInheritanceStatus())

    def testSelectDeleteInheritanceSetsFlag(self):
        self.controller._InheritanceContextMenuController__selectDeleteInheritance()
        self.assertTrue(self.controller.getSelectDeleteInheritanceStatus())

    def testUnselectDeleteInheritanceClearsFlag(self):
        self.controller._InheritanceContextMenuController__selectDeleteInheritance()
        self.controller.unselectDeleteInheritance()
        self.assertFalse(self.controller.getSelectDeleteInheritanceStatus())

    def testSignalsConnectedOnInit(self):
        self.view.actionDeleteInheritance.triggered.connect.assert_called_with(
            self.controller._InheritanceContextMenuController__selectDeleteInheritance
        )


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
