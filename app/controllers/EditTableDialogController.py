from PySide6.QtWidgets import QTableView
from copy import deepcopy

from app.views.ErrorDialogView import ErrorDialogView
from app.models.TableColumnsModel import TableColumnsModel


class EditTableDialogController:
    def __init__(self, EditTableDialogView, TablesController, ObtainedTable):
        self.__EditTableDialogView = EditTableDialogView
        self.__TablesController = TablesController
        self.__ObtainedTable = ObtainedTable

        ObtainedTableColumnsModel = ObtainedTable.getTableColumnsModel()
        originalColumns = ObtainedTableColumnsModel.getColumns()
        copiedColumns = deepcopy(originalColumns)

        self.__TempTableColumnsModel = TableColumnsModel(copiedColumns)
        self.__EditTableDialogView.tableView.setModel(self.__TempTableColumnsModel)

        self.__EditTableDialogView.addColumnButton.clicked.connect(self.__selectAddColumn)
        self.__EditTableDialogView.deleteColumnButton.clicked.connect(self.__selectDeleteColumn)
        self.__EditTableDialogView.editColumnButton.clicked.connect(self.__toggleEditColumns)
        self.__EditTableDialogView.cancelButton.clicked.connect(self.__selectCancel)
        self.__EditTableDialogView.okButton.clicked.connect(self.__selectOK)

    def __selectAddColumn(self):
        columnName = self.__EditTableDialogView.columnNameLineEdit.text()
        dataType = self.__EditTableDialogView.dataTypeComboBox.currentText()
        length = self.__EditTableDialogView.lengthSpinBox.value()

        if columnName == "":
            dialogTitle = "ERROR"
            dialogText = f"Column Name is Empty"
            ErrorDialog = ErrorDialogView(self.__EditTableDialogView, dialogTitle, dialogText)
            ErrorDialog.displayDialog()
        else:
            self.__TempTableColumnsModel.addColumn(columnName, dataType, length)

            self.__EditTableDialogView.columnNameLineEdit.clear()
            self.__EditTableDialogView.dataTypeComboBox.setCurrentIndex(0)
            self.__EditTableDialogView.lengthSpinBox.setValue(0)

    def __selectDeleteColumn(self):
        selectedRows = self.__EditTableDialogView.tableView.selectionModel().selectedRows()
        if selectedRows:
            selectedRowNumber = selectedRows[0].row()
            self.__TempTableColumnsModel.deleteColumn(selectedRowNumber)

    def __toggleEditColumns(self):
        self.__TempTableColumnsModel.toggleEditColumns()
        if self.__TempTableColumnsModel.getEditColumnsStatus():
            self.__EditTableDialogView.tableView.setEditTriggers(
                QTableView.EditTrigger.DoubleClicked | QTableView.EditTrigger.SelectedClicked
            )
            self.__EditTableDialogView.editColumnButton.setText(u"Disable Editing Mode")
        else:
            self.__EditTableDialogView.tableView.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
            self.__EditTableDialogView.editColumnButton.setText(u"Enable Editing Mode")

    def __selectCancel(self):
        self.__EditTableDialogView.reject()

    def __selectOK(self):
        if self.__editTableName():
            self.__editTableColumns()
            self.__editTableDimensions()
            self.__EditTableDialogView.accept()

    def __editTableName(self):
        newName = self.__EditTableDialogView.tableNameLineEdit.text()

        if newName == self.__ObtainedTable.getTableName():
            return True

        if newName == "":
            dialogText = f"Table Name is Empty"
        elif self.__TablesController.checkTableNameUnique(newName):
            self.__ObtainedTable.editTableName(newName)
            return True
        else:
            dialogText = f"Table Name is not Unique"

        dialogTitle = "ERROR"
        ErrorDialog = ErrorDialogView(self.__EditTableDialogView, dialogTitle, dialogText)
        ErrorDialog.displayDialog()

        return False

    def __editTableColumns(self):
        self.__ObtainedTable.changeTableColumnsModel(self.__TempTableColumnsModel)

    def __editTableDimensions(self):
        self.__ObtainedTable.changeTableDimensions()
