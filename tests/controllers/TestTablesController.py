import unittest
from unittest.mock import MagicMock, patch

from app.controllers.TablesController import TablesController
from app.enums.TableContextMenuEnum import TableContextMenuEnum


class TestTablesController(unittest.TestCase):
    def setUp(self):
        self.parentWindow = MagicMock()
        self.tablesView = MagicMock()
        self.tablesModel = MagicMock()
        self.relationshipsController = MagicMock()
        self.inheritancesController = MagicMock()

        table_context_patcher = patch('app.controllers.TablesController.TableContextMenuView')
        self.MockTableContextMenuView = table_context_patcher.start()
        self.addCleanup(table_context_patcher.stop)

        self.mockContextMenuViewInstance = MagicMock()
        self.MockTableContextMenuView.return_value = self.mockContextMenuViewInstance

        self.controller = TablesController(
            self.parentWindow,
            self.tablesView,
            self.tablesModel,
            self.relationshipsController,
            self.inheritancesController
        )

    def testAddTableCallsModel(self):
        pos = MagicMock()
        self.controller.addTable(pos)
        self.tablesModel.addTable.assert_called_once_with(pos)

    def testDeleteTableConfirmed(self):
        pos = MagicMock()
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        with patch('app.controllers.TablesController.ConfirmationDialogView') as MockDialog:
            mockDialogInstance = MockDialog.return_value
            mockDialogInstance.displayDialog.return_value = True

            self.controller.deleteTable(pos)

            self.tablesModel.deleteSelectedTable.assert_called_once_with(mockTable)
            self.relationshipsController.deleteRelationshipByTable.assert_called_once_with(mockTable)
            self.inheritancesController.deleteInheritanceByTable.assert_called_once_with(mockTable)

    def testDeleteTableNotConfirmed(self):
        pos = MagicMock()
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        with patch('app.controllers.TablesController.ConfirmationDialogView') as MockDialog:
            mockDialogInstance = MockDialog.return_value
            mockDialogInstance.displayDialog.return_value = False

            self.controller.deleteTable(pos)

            self.tablesModel.deleteSelectedTable.assert_not_called()
            self.relationshipsController.deleteRelationshipByTable.assert_not_called()
            self.inheritancesController.deleteInheritanceByTable.assert_not_called()

    def testEditTableOpensDialog(self):
        pos = MagicMock()
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        with patch('app.controllers.TablesController.EditTableDialogView') as MockEditDialogView:
            with patch('app.controllers.TablesController.EditTableDialogController') as MockEditDialogController:
                mockDialogInstance = MockEditDialogView.return_value

                self.controller.editTable(pos)

                MockEditDialogView.assert_called_once_with(self.parentWindow, mockTable)
                mockDialogInstance.setupUi.assert_called_once()
                MockEditDialogController.assert_called_once_with(
                    mockDialogInstance,
                    self.controller,
                    mockTable
                )
                mockDialogInstance.displayDialog.assert_called_once()

    def testSelectAndUnselectTableInTransfer(self):
        pos = MagicMock()
        pos.x.return_value = 10
        pos.y.return_value = 20
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        self.controller.selectTableInTransfer(pos)
        self.assertTrue(self.controller.getTableInTransferStatus())
        self.assertIs(self.controller._TablesController__TableInTransfer, mockTable)

        self.controller.unselectTableInTransfer(pos)
        mockTable.changeTablePosition.assert_called_once_with(10, 20)
        self.assertFalse(self.controller.getTableInTransferStatus())
        self.assertIsNone(self.controller._TablesController__TableInTransfer)

    def testUpdateTableInTransferPosition(self):
        mockTable = MagicMock()
        self.controller._TablesController__TableInTransfer = mockTable

        pos = MagicMock()
        pos.x.return_value = 5
        pos.y.return_value = 6

        self.controller.updateTableInTransferPosition(pos)

        mockTable.changeTablePosition.assert_called_once_with(5, 6)

    def testDrawMethodsCalled(self):
        pos = MagicMock()
        self.controller.selectDrawTempTable(pos)
        self.tablesView.drawTempTable.assert_called_once_with(pos)

        self.controller.selectDrawTables()
        self.tablesView.drawTables.assert_called_once()

    def testDisplayTableContextMenuCollapse(self):
        pos = MagicMock()
        globalPos = MagicMock()
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        cm_controller = self.controller._TablesController__TableContextMenuController
        cm_controller.getSelectCollapseTableStatus = MagicMock(return_value=True)
        cm_controller.getSelectEditTableStatus = MagicMock(return_value=False)
        cm_controller.getSelectDeleteTableStatus = MagicMock(return_value=False)
        cm_controller.unselectCollapseTable = MagicMock()

        result = self.controller.displayTableContextMenu(pos, globalPos)

        self.mockContextMenuViewInstance.exec.assert_called_once_with(globalPos)
        cm_controller.unselectCollapseTable.assert_called_once()
        self.assertEqual(result, TableContextMenuEnum.COLLAPSE)
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())

    def testDisplayTableContextMenuEdit(self):
        pos = MagicMock()
        globalPos = MagicMock()
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        cm_controller = self.controller._TablesController__TableContextMenuController
        cm_controller.getSelectCollapseTableStatus = MagicMock(return_value=False)
        cm_controller.getSelectEditTableStatus = MagicMock(return_value=True)
        cm_controller.getSelectDeleteTableStatus = MagicMock(return_value=False)
        cm_controller.unselectEditTable = MagicMock()

        result = self.controller.displayTableContextMenu(pos, globalPos)

        self.mockContextMenuViewInstance.exec.assert_called_once_with(globalPos)
        cm_controller.unselectEditTable.assert_called_once()
        self.assertEqual(result, TableContextMenuEnum.EDIT)
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())

    def testDisplayTableContextMenuDelete(self):
        pos = MagicMock()
        globalPos = MagicMock()
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        cm_controller = self.controller._TablesController__TableContextMenuController
        cm_controller.getSelectCollapseTableStatus = MagicMock(return_value=False)
        cm_controller.getSelectEditTableStatus = MagicMock(return_value=False)
        cm_controller.getSelectDeleteTableStatus = MagicMock(return_value=True)
        cm_controller.unselectDeleteTable = MagicMock()

        result = self.controller.displayTableContextMenu(pos, globalPos)

        self.mockContextMenuViewInstance.exec.assert_called_once_with(globalPos)
        cm_controller.unselectDeleteTable.assert_called_once()
        self.assertEqual(result, TableContextMenuEnum.DELETE)
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())

    def testDisplayTableContextMenuNone(self):
        pos = MagicMock()
        globalPos = MagicMock()
        mockTable = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = mockTable

        cm_controller = self.controller._TablesController__TableContextMenuController
        cm_controller.getSelectCollapseTableStatus = MagicMock(return_value=False)
        cm_controller.getSelectEditTableStatus = MagicMock(return_value=False)
        cm_controller.getSelectDeleteTableStatus = MagicMock(return_value=False)

        result = self.controller.displayTableContextMenu(pos, globalPos)

        self.mockContextMenuViewInstance.exec.assert_called_once_with(globalPos)
        self.assertEqual(result, TableContextMenuEnum.NONE)
        self.assertTrue(self.controller.getContextMenuAtWorkStatus())

    def testDisplayTableContextMenuNoTable(self):
        pos = MagicMock()
        globalPos = MagicMock()
        self.tablesModel.getTableFromPosition.return_value = None

        result = self.controller.displayTableContextMenu(pos, globalPos)

        self.assertIsNone(result)
        self.mockContextMenuViewInstance.exec.assert_not_called()

    def testUnselectContextMenuAtWork(self):
        self.controller._TablesController__isContextMenuAtWork = True
        self.controller.unselectContextMenuAtWork()
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())

    def testGetContextMenuAtWorkStatus(self):
        self.controller._TablesController__isContextMenuAtWork = True
        self.assertTrue(self.controller.getContextMenuAtWorkStatus())
        self.controller._TablesController__isContextMenuAtWork = False
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
