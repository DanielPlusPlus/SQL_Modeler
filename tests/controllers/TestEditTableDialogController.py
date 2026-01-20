import unittest
from unittest.mock import MagicMock, patch

from app.controllers.EditTableDialogController import EditTableDialogController


class TestEditTableDialogController(unittest.TestCase):

    @patch('app.controllers.EditTableDialogController.TableColumnsModel')
    @patch('app.controllers.EditTableDialogController.deepcopy')
    def setUp(self, mockDeepcopy, mockTableColumnsModelClass):
        self.mockEditTableDialogView = MagicMock()
        self.mockEditTableDialogView.tableView = MagicMock()
        self.mockEditTableDialogView.tableView.selectionModel.return_value.selectedRows.return_value = []
        self.mockEditTableDialogView.columnNameLineEdit = MagicMock()
        self.mockEditTableDialogView.dataTypeComboBox = MagicMock()
        self.mockEditTableDialogView.lengthSpinBox = MagicMock()
        self.mockEditTableDialogView.addColumnButton = MagicMock()
        self.mockEditTableDialogView.deleteColumnButton = MagicMock()
        self.mockEditTableDialogView.editColumnButton = MagicMock()
        self.mockEditTableDialogView.cancelButton = MagicMock()
        self.mockEditTableDialogView.okButton = MagicMock()
        self.mockEditTableDialogView.tableNameLineEdit = MagicMock()

        self.mockTablesController = MagicMock()

        self.mockObtainedTable = MagicMock()
        self.mockObtainedTableColumnsModelFromTable = MagicMock()
        self.mockObtainedTable.getTableColumnsModel.return_value = self.mockObtainedTableColumnsModelFromTable

        self.originalColumnsData = [
            {
                'name': 'id',
                'data_type': 'INT',
                'length': 11,
                'is_pk': True,
                'is_fk': False,
                'is_unique': True,
                'is_nullable': False,
                'default_value': None
            },
            {
                'name': 'name',
                'data_type': 'VARCHAR',
                'length': 255,
                'is_pk': False,
                'is_fk': False,
                'is_unique': False,
                'is_nullable': True,
                'default_value': 'N/A'
            }
        ]
        self.mockObtainedTableColumnsModelFromTable.getColumns.return_value = self.originalColumnsData

        self.copiedColumnsData = list(self.originalColumnsData)
        mockDeepcopy.return_value = self.copiedColumnsData
        self.mockDeepcopy = mockDeepcopy

        self.mockTempTableColumnsModelInstance = MagicMock()
        mockTableColumnsModelClass.return_value = self.mockTempTableColumnsModelInstance
        self.mockTableColumnsModelClass = mockTableColumnsModelClass

        self.controller = EditTableDialogController(
            self.mockEditTableDialogView,
            self.mockTablesController,
            self.mockObtainedTable
        )

    def testConstructorAssignments(self):
        self.assertIs(
            self.controller._EditTableDialogController__EditTableDialogView,
            self.mockEditTableDialogView
        )
        self.assertIs(
            self.controller._EditTableDialogController__TablesController,
            self.mockTablesController
        )
        self.assertIs(
            self.controller._EditTableDialogController__ObtainedTable,
            self.mockObtainedTable
        )

        self.mockObtainedTable.getTableColumnsModel.assert_called_once()
        self.mockObtainedTableColumnsModelFromTable.getColumns.assert_called_once()
        self.mockDeepcopy.assert_called_once_with(self.originalColumnsData)

        self.mockTableColumnsModelClass.assert_called_once_with(self.copiedColumnsData)
        self.assertIs(
            self.controller._EditTableDialogController__TempTableColumnsModel,
            self.mockTempTableColumnsModelInstance
        )
        self.mockEditTableDialogView.tableView.setModel.assert_called_once_with(
            self.mockTempTableColumnsModelInstance
        )

        self.mockEditTableDialogView.addColumnButton.clicked.connect.assert_called_once_with(
            self.controller._EditTableDialogController__selectAddColumn
        )
        self.mockEditTableDialogView.deleteColumnButton.clicked.connect.assert_called_once_with(
            self.controller._EditTableDialogController__selectDeleteColumn
        )
        self.mockEditTableDialogView.editColumnButton.clicked.connect.assert_called_once_with(
            self.controller._EditTableDialogController__toggleEditColumns
        )
        self.mockEditTableDialogView.cancelButton.clicked.connect.assert_called_once_with(
            self.controller._EditTableDialogController__selectCancel
        )
        self.mockEditTableDialogView.okButton.clicked.connect.assert_called_once_with(
            self.controller._EditTableDialogController__selectOK
        )

    @patch('app.controllers.EditTableDialogController.ErrorDialogView')
    def testSelectAddColumn_validData(self, mockErrorDialogViewClass):
        self.mockEditTableDialogView.columnNameLineEdit.text.return_value = "new_column"
        self.mockEditTableDialogView.dataTypeComboBox.currentText.return_value = "TEXT"
        self.mockEditTableDialogView.lengthSpinBox.value.return_value = 50

        self.controller._EditTableDialogController__selectAddColumn()

        mockErrorDialogViewClass.assert_not_called()

        self.mockTempTableColumnsModelInstance.addColumn.assert_called_once_with(
            "new_column", "TEXT", 50
        )

        self.mockEditTableDialogView.columnNameLineEdit.clear.assert_called_once()
        self.mockEditTableDialogView.dataTypeComboBox.setCurrentIndex.assert_called_once_with(0)
        self.mockEditTableDialogView.lengthSpinBox.setValue.assert_called_once_with(0)

    @patch('app.controllers.EditTableDialogController.ErrorDialogView')
    def testSelectAddColumn_emptyName_showsError(self, mockErrorDialogViewClass):
        self.mockEditTableDialogView.columnNameLineEdit.text.return_value = ""
        self.mockEditTableDialogView.dataTypeComboBox.currentText.return_value = "TEXT"
        self.mockEditTableDialogView.lengthSpinBox.value.return_value = 50

        self.controller._EditTableDialogController__selectAddColumn()

        self.mockTempTableColumnsModelInstance.addColumn.assert_not_called()

        mockErrorDialogViewClass.assert_called_once()
        instance = mockErrorDialogViewClass.return_value
        instance.displayDialog.assert_called_once()

    def testSelectDeleteColumnWithSelection(self):
        mockSelectedRowIndex = MagicMock()
        mockSelectedRowIndex.row.return_value = 1
        self.mockEditTableDialogView.tableView.selectionModel.return_value.selectedRows.return_value = [
            mockSelectedRowIndex
        ]

        self.controller._EditTableDialogController__selectDeleteColumn()

        self.mockTempTableColumnsModelInstance.deleteColumn.assert_called_once_with(1)

    def testSelectDeleteColumnNoSelection(self):
        self.mockEditTableDialogView.tableView.selectionModel.return_value.selectedRows.return_value = []

        self.controller._EditTableDialogController__selectDeleteColumn()

        self.mockTempTableColumnsModelInstance.deleteColumn.assert_not_called()

    def testToggleEditColumns_enablesAndDisables(self):
        self.mockTempTableColumnsModelInstance.getEditColumnsStatus.return_value = True

        self.controller._EditTableDialogController__toggleEditColumns()

        self.mockTempTableColumnsModelInstance.toggleEditColumns.assert_called_once()
        self.mockEditTableDialogView.tableView.setEditTriggers.assert_called_once()
        self.mockEditTableDialogView.editColumnButton.setText.assert_called_once_with(
            u"Disable Editing Mode"
        )

        self.mockTempTableColumnsModelInstance.toggleEditColumns.reset_mock()
        self.mockEditTableDialogView.tableView.setEditTriggers.reset_mock()
        self.mockEditTableDialogView.editColumnButton.setText.reset_mock()

        self.mockTempTableColumnsModelInstance.getEditColumnsStatus.return_value = False

        self.controller._EditTableDialogController__toggleEditColumns()

        self.mockTempTableColumnsModelInstance.toggleEditColumns.assert_called_once()
        self.mockEditTableDialogView.tableView.setEditTriggers.assert_called_once()
        self.mockEditTableDialogView.editColumnButton.setText.assert_called_once_with(
            u"Enable Editing Mode"
        )

    def testSelectCancel(self):
        self.controller._EditTableDialogController__selectCancel()
        self.mockEditTableDialogView.reject.assert_called_once()

    def testSelectOK_editTableNameReturnsTrue(self):
        self.controller._EditTableDialogController__editTableName = MagicMock(return_value=True)
        self.controller._EditTableDialogController__editTableColumns = MagicMock()
        self.controller._EditTableDialogController__editTableDimensions = MagicMock()

        self.controller._EditTableDialogController__selectOK()

        self.controller._EditTableDialogController__editTableName.assert_called_once()
        self.controller._EditTableDialogController__editTableColumns.assert_called_once()
        self.controller._EditTableDialogController__editTableDimensions.assert_called_once()
        self.mockEditTableDialogView.accept.assert_called_once()

    def testSelectOK_editTableNameReturnsFalse(self):
        self.controller._EditTableDialogController__editTableName = MagicMock(return_value=False)
        self.controller._EditTableDialogController__editTableColumns = MagicMock()
        self.controller._EditTableDialogController__editTableDimensions = MagicMock()

        self.controller._EditTableDialogController__selectOK()

        self.controller._EditTableDialogController__editTableName.assert_called_once()
        self.controller._EditTableDialogController__editTableColumns.assert_not_called()
        self.controller._EditTableDialogController__editTableDimensions.assert_not_called()
        self.mockEditTableDialogView.accept.assert_not_called()

    @patch('app.controllers.EditTableDialogController.ErrorDialogView')
    def testEditTableName_sameName_returnsTrueNoDialog(self, mockErrorDialogViewClass):
        oldName = "Table1"
        self.mockObtainedTable.getTableName.return_value = oldName
        self.mockEditTableDialogView.tableNameLineEdit.text.return_value = oldName

        result = self.controller._EditTableDialogController__editTableName()

        self.assertTrue(result)
        self.mockTablesController.checkTableNameUnique.assert_not_called()
        self.mockObtainedTable.editTableName.assert_not_called()
        mockErrorDialogViewClass.assert_not_called()

    @patch('app.controllers.EditTableDialogController.ErrorDialogView')
    def testEditTableName_emptyName_showsErrorAndReturnsFalse(self, mockErrorDialogViewClass):
        self.mockObtainedTable.getTableName.return_value = "OldName"
        self.mockEditTableDialogView.tableNameLineEdit.text.return_value = ""

        result = self.controller._EditTableDialogController__editTableName()

        self.assertFalse(result)
        self.mockTablesController.checkTableNameUnique.assert_not_called()
        self.mockObtainedTable.editTableName.assert_not_called()
        mockErrorDialogViewClass.assert_called_once()
        instance = mockErrorDialogViewClass.return_value
        instance.displayDialog.assert_called_once()

    @patch('app.controllers.EditTableDialogController.ErrorDialogView')
    def testEditTableName_uniqueName_editsAndReturnsTrue(self, mockErrorDialogViewClass):
        self.mockObtainedTable.getTableName.return_value = "OldName"
        newName = "NewUniqueName"
        self.mockEditTableDialogView.tableNameLineEdit.text.return_value = newName
        self.mockTablesController.checkTableNameUnique.return_value = True

        result = self.controller._EditTableDialogController__editTableName()

        self.assertTrue(result)
        self.mockTablesController.checkTableNameUnique.assert_called_once_with(newName)
        self.mockObtainedTable.editTableName.assert_called_once_with(newName)
        mockErrorDialogViewClass.assert_not_called()

    @patch('app.controllers.EditTableDialogController.ErrorDialogView')
    def testEditTableName_notUnique_showsErrorAndReturnsFalse(self, mockErrorDialogViewClass):
        self.mockObtainedTable.getTableName.return_value = "OldName"
        newName = "NewName"
        self.mockEditTableDialogView.tableNameLineEdit.text.return_value = newName
        self.mockTablesController.checkTableNameUnique.return_value = False

        result = self.controller._EditTableDialogController__editTableName()

        self.assertFalse(result)
        self.mockTablesController.checkTableNameUnique.assert_called_once_with(newName)
        self.mockObtainedTable.editTableName.assert_not_called()
        mockErrorDialogViewClass.assert_called_once()
        instance = mockErrorDialogViewClass.return_value
        instance.displayDialog.assert_called_once()

    def testEditTableColumns(self):
        self.controller._EditTableDialogController__editTableColumns()
        self.mockObtainedTable.changeTableColumnsModel.assert_called_once_with(
            self.mockTempTableColumnsModelInstance
        )

    def testEditTableDimensions(self):
        self.controller._EditTableDialogController__editTableDimensions()
        self.mockObtainedTable.changeTableDimensions.assert_called_once()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)