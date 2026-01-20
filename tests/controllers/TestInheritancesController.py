import unittest
from unittest.mock import MagicMock, patch

from app.controllers.InheritancesController import InheritancesController
from app.enums.InheritanceContextMenuEnum import InheritanceContextMenuEnum


class TestInheritancesController(unittest.TestCase):

    @patch("app.controllers.InheritancesController.InheritanceContextMenuView")
    @patch("app.controllers.InheritancesController.InheritanceContextMenuController")
    def setUp(self, MockContextMenuController, MockContextMenuView):
        self.mockParentWindow = MagicMock()
        self.mockInheritanceView = MagicMock()
        self.mockInheritanceModel = MagicMock()
        self.mockTablesModel = MagicMock()

        self.mockContextMenuView = MockContextMenuView.return_value
        self.mockContextMenuController = MockContextMenuController.return_value

        self.controller = InheritancesController(
            self.mockParentWindow,
            self.mockInheritanceView,
            self.mockInheritanceModel,
            self.mockTablesModel
        )

    def testSelectInheritanceBeingDrawn(self):
        self.controller.selectInheritanceBeingDrawn()
        self.assertTrue(self.controller.getInheritanceBeingDrawnStatus())

    def testUnselectInheritanceBeingDrawn(self):
        self.controller.selectInheritanceBeingDrawn()
        self.controller.unselectInheritanceBeingDrawn()
        self.assertFalse(self.controller.getInheritanceBeingDrawnStatus())

    def testAddInheritanceCallsModelAndResetsTables(self):
        self.controller._FirstClickedTable = "Table1"
        self.controller._SecondClickedTable = "Table2"
        self.controller.resetTables = MagicMock()

        self.controller.addInheritance()

        self.mockInheritanceModel.addInheritance.assert_called_once_with("Table1", "Table2")
        self.controller.resetTables.assert_called_once()

    @patch("app.controllers.InheritancesController.ConfirmationDialogView")
    def testDeleteInheritanceWithConfirmation(self, MockConfirmationDialog):
        cursorPos = (10, 20)
        mockInheritance = MagicMock()
        self.mockInheritanceModel.getInheritanceFromPosition.return_value = mockInheritance

        instance = MockConfirmationDialog.return_value
        instance.displayDialog.return_value = True

        self.controller.deleteInheritance(cursorPos)

        self.mockInheritanceModel.deleteSelectedInheritance.assert_called_once_with(mockInheritance)
        instance.displayDialog.assert_called_once()

    @patch("app.controllers.InheritancesController.ConfirmationDialogView")
    def testDeleteInheritanceCancelled(self, MockConfirmationDialog):
        cursorPos = (10, 20)
        mockInheritance = MagicMock()
        self.mockInheritanceModel.getInheritanceFromPosition.return_value = mockInheritance

        instance = MockConfirmationDialog.return_value
        instance.displayDialog.return_value = False

        self.controller.deleteInheritance(cursorPos)

        self.mockInheritanceModel.deleteSelectedInheritance.assert_not_called()
        instance.displayDialog.assert_called_once()

    def testDeleteInheritanceNone(self):
        cursorPos = (10, 20)
        self.mockInheritanceModel.getInheritanceFromPosition.return_value = None

        self.controller.deleteInheritance(cursorPos)

        self.mockInheritanceModel.deleteSelectedInheritance.assert_not_called()

    def testDeleteInheritanceByTableCallsModel(self):
        mockTable = MagicMock()
        self.controller.deleteInheritanceByTable(mockTable)
        self.mockInheritanceModel.deleteInheritanceByTable.assert_called_once_with(mockTable)

    def testDisplayInheritanceContextMenuDelete(self):
        cursorPos = (10, 20)
        globalPos = (100, 200)
        mockInheritance = MagicMock()
        self.mockInheritanceModel.getInheritanceFromPosition.return_value = mockInheritance
        self.mockContextMenuController.getSelectDeleteInheritanceStatus.return_value = True

        result = self.controller.displayInheritanceContextMenu(cursorPos, globalPos)

        self.mockContextMenuView.exec.assert_called_once_with(globalPos)
        self.mockContextMenuController.unselectDeleteInheritance.assert_called_once()
        self.assertEqual(result, InheritanceContextMenuEnum.DELETE)
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())

    def testDisplayInheritanceContextMenuNone(self):
        cursorPos = (10, 20)
        globalPos = (100, 200)
        mockInheritance = MagicMock()
        self.mockInheritanceModel.getInheritanceFromPosition.return_value = mockInheritance
        self.mockContextMenuController.getSelectDeleteInheritanceStatus.return_value = False

        result = self.controller.displayInheritanceContextMenu(cursorPos, globalPos)

        self.mockContextMenuView.exec.assert_called_once_with(globalPos)
        self.assertEqual(result, InheritanceContextMenuEnum.NONE)
        self.assertTrue(self.controller.getContextMenuAtWorkStatus())

    def testDisplayInheritanceContextMenuNoInheritance(self):
        cursorPos = (10, 20)
        globalPos = (100, 200)
        self.mockInheritanceModel.getInheritanceFromPosition.return_value = None

        result = self.controller.displayInheritanceContextMenu(cursorPos, globalPos)
        self.assertIsNone(result)
        self.mockContextMenuView.exec.assert_not_called()

    def testContextMenuAtWorkStatusMethods(self):
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())
        self.controller.unselectContextMenuAtWork()
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
