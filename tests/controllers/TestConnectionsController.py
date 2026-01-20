import unittest
from unittest.mock import MagicMock
import sys

from app.controllers.ConnectionsController import ConnectionsController


class TestConnectionsController(unittest.TestCase):

    def setUp(self):
        if 'app.controllers.ConnectionsController' in sys.modules:
            del sys.modules['app.controllers.ConnectionsController']

        self.mockTablesModel = MagicMock()
        self.mockParentWindow = MagicMock()
        self.controller = ConnectionsController(self.mockParentWindow, self.mockTablesModel)

    def testInitialState(self):
        self.assertIsNone(self.controller._FirstClickedTable)
        self.assertIsNone(self.controller._SecondClickedTable)
        self.assertEqual(self.controller._ParentWindow, self.mockParentWindow)
        self.assertEqual(self.controller._ConnectionsController__TablesModel, self.mockTablesModel)

    def testSetFirstClickedTableFound(self):
        mockTable = MagicMock()
        cursorPosition = (10, 20)
        self.mockTablesModel.getTableFromPosition.return_value = mockTable
        result = self.controller.setFirstClickedTable(cursorPosition)
        self.mockTablesModel.getTableFromPosition.assert_called_once_with(cursorPosition)
        self.assertEqual(self.controller._FirstClickedTable, mockTable)
        self.assertTrue(result)

    def testSetFirstClickedTableNotFound(self):
        cursorPosition = (10, 20)
        self.mockTablesModel.getTableFromPosition.return_value = None
        result = self.controller.setFirstClickedTable(cursorPosition)
        self.mockTablesModel.getTableFromPosition.assert_called_once_with(cursorPosition)
        self.assertIsNone(self.controller._FirstClickedTable)
        self.assertFalse(result)

    def testSetSecondClickedTableFound(self):
        mockTable = MagicMock()
        cursorPosition = (30, 40)
        self.mockTablesModel.getTableFromPosition.return_value = mockTable
        result = self.controller.setSecondClickedTable(cursorPosition)
        self.mockTablesModel.getTableFromPosition.assert_called_once_with(cursorPosition)
        self.assertEqual(self.controller._SecondClickedTable, mockTable)
        self.assertTrue(result)

    def testSetSecondClickedTableNotFound(self):
        cursorPosition = (30, 40)
        self.mockTablesModel.getTableFromPosition.return_value = None
        result = self.controller.setSecondClickedTable(cursorPosition)
        self.mockTablesModel.getTableFromPosition.assert_called_once_with(cursorPosition)
        self.assertIsNone(self.controller._SecondClickedTable)
        self.assertFalse(result)

    def testResetTables(self):
        self.controller._FirstClickedTable = MagicMock()
        self.controller._SecondClickedTable = MagicMock()
        self.controller.resetTables()
        self.assertIsNone(self.controller._FirstClickedTable)
        self.assertIsNone(self.controller._SecondClickedTable)


if __name__ == '__main__':
    unittest.main()
