import unittest
from unittest.mock import MagicMock

from app.controllers.TableContextMenuController import TableContextMenuController


class TestTableContextMenuController(unittest.TestCase):
    def setUp(self):
        self.mockView = MagicMock()
        self.mockView.actionCollapseTable = MagicMock()
        self.mockView.actionCollapseTable.triggered.connect = MagicMock()
        self.mockView.actionEditTable = MagicMock()
        self.mockView.actionEditTable.triggered.connect = MagicMock()
        self.mockView.actionDeleteTable = MagicMock()
        self.mockView.actionDeleteTable.triggered.connect = MagicMock()

        self.controller = TableContextMenuController(self.mockView)

    def testInitialState(self):
        self.assertFalse(self.controller.getSelectCollapseTableStatus())
        self.assertFalse(self.controller.getSelectEditTableStatus())
        self.assertFalse(self.controller.getSelectDeleteTableStatus())

    def testSelectCollapseTable(self):
        self.controller._TableContextMenuController__selectCollapseTable()
        self.assertTrue(self.controller.getSelectCollapseTableStatus())

    def testUnselectCollapseTable(self):
        self.controller._TableContextMenuController__selectCollapseTable()
        self.controller.unselectCollapseTable()
        self.assertFalse(self.controller.getSelectCollapseTableStatus())

    def testSelectEditTable(self):
        self.controller._TableContextMenuController__selectEditTable()
        self.assertTrue(self.controller.getSelectEditTableStatus())

    def testUnselectEditTable(self):
        self.controller._TableContextMenuController__selectEditTable()
        self.controller.unselectEditTable()
        self.assertFalse(self.controller.getSelectEditTableStatus())

    def testSelectDeleteTable(self):
        self.controller._TableContextMenuController__selectDeleteTable()
        self.assertTrue(self.controller.getSelectDeleteTableStatus())

    def testUnselectDeleteTable(self):
        self.controller._TableContextMenuController__selectDeleteTable()
        self.controller.unselectDeleteTable()
        self.assertFalse(self.controller.getSelectDeleteTableStatus())

    def testSignalConnections(self):
        self.mockView.actionCollapseTable.triggered.connect.assert_called_with(
            self.controller._TableContextMenuController__selectCollapseTable
        )
        self.mockView.actionEditTable.triggered.connect.assert_called_with(
            self.controller._TableContextMenuController__selectEditTable
        )
        self.mockView.actionDeleteTable.triggered.connect.assert_called_with(
            self.controller._TableContextMenuController__selectDeleteTable
        )


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
