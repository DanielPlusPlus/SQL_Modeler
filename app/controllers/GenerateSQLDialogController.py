from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFileDialog, QDialog

from app.views.patterns.ConnectionParamsDialogViewsFactory import ConnectionParamsDialogViewsFactory
from app.views.InfoDialogView import InfoDialogView
from app.views.ErrorDialogView import ErrorDialogView
from app.views.ExecutionSQLDialogView import ExecutionSQLDialogView
from app.controllers.patterns.ConnectionParamsDialogControllersFactory import ConnectionParamsDialogControllersFactory
from app.controllers.patterns.DatabaseControllersFactory import DatabaseControllersFactory
from app.controllers.ExecutionSQLDialogController import ExecutionSQLDialogController
from app.enums.DatabasesEnum import DatabasesEnum


class GenerateSQLDialogController:
    def __init__(self, ParentWindow, MainWindowController, GenerateSQLDialogView):
        self.__ParentWindow = ParentWindow
        self.__MainWindowController = MainWindowController
        self.__GenerateSQLDialogView = GenerateSQLDialogView

        self.__GenerateSQLDialogView.copyCodeButton.clicked.connect(self.__selectCopyCode)
        self.__GenerateSQLDialogView.saveCodeButton.clicked.connect(self.__selectSaveCode)
        self.__GenerateSQLDialogView.testCodeButton.clicked.connect(self.__selectTestCode)
        self.__GenerateSQLDialogView.cancelButton.clicked.connect(self.__selectCancel)
        self.__GenerateSQLDialogView.okButton.clicked.connect(self.__selectOK)

    def __selectCopyCode(self):
        clipboard = QGuiApplication.clipboard()
        sqlCode = self.__getSelectedSQLCode()

        clipboard.setText(sqlCode)

        dialogTitle = "INFORMATION"
        dialogText = "Entire SQL code has been copied to clipboard"
        InfoDialog = InfoDialogView(self.__ParentWindow, dialogTitle, dialogText)
        InfoDialog.displayDialog()

    def __selectSaveCode(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self.__GenerateSQLDialogView,
            "Save SQL Code",
            filter="SQL Files (*.sql)"
        )
        if filePath:
            try:
                sqlCode = self.__getSelectedSQLCode()
                with open(filePath, 'w', encoding='utf-8') as file:
                    file.write(sqlCode)
                    dialogTitle = "INFORMATION"
                    dialogText = "SQL code has been successfully saved to a file"
                    InfoDialog = InfoDialogView(self.__ParentWindow, dialogTitle, dialogText)
                    InfoDialog.displayDialog()
                    self.__MainWindowController.selectCloseWithoutConfirmation()
            except Exception as e:
                dialogTitle = "ERROR"
                dialogText = f"Failed to save file:\n{str(e)}"
                ErrorDialog = ErrorDialogView(self.__ParentWindow, dialogTitle, dialogText)
                ErrorDialog.displayDialog()

    def __selectTestCode(self):
        DatabaseType = self.__getSelectedDatabaseType()
        ConnectionParamsDialog = ConnectionParamsDialogViewsFactory.createController(self.__ParentWindow,
                                                                                     DatabaseType)
        ConnectionParamsDialog.setupUI()
        ConnectionParamsControl = ConnectionParamsDialogControllersFactory.createController(ConnectionParamsDialog,
                                                                                            DatabaseType)
        if ConnectionParamsDialog.displayDialog() == QDialog.Accepted:
            connectionParams = ConnectionParamsControl.getConnectionParams()
            sqlCode = self.__getSelectedSQLCode()

            if not sqlCode.strip():
                dialogTitle = "ERROR"
                dialogText = "SQL code is empty"
                ErrorDialog = ErrorDialogView(self.__ParentWindow, dialogTitle, dialogText)
                ErrorDialog.displayDialog()
                return

            DatabaseControl = DatabaseControllersFactory.createController(connectionParams, DatabaseType)
            executionResult = DatabaseControl.executeSQLCode(sqlCode)

            ExecutionSQLDialog = ExecutionSQLDialogView(self.__ParentWindow)
            ExecutionSQLDialog.setupUI(executionResult)
            ExecutionSQLControl = ExecutionSQLDialogController(ExecutionSQLDialog)
            ExecutionSQLDialog.displayDialog()

    def __getSelectedDatabaseType(self):
        return DatabasesEnum(self.__GenerateSQLDialogView.TabWidget.currentIndex() + 1)

    def __getSelectedSQLCode(self):
        currentEditor = self.__GenerateSQLDialogView.TabWidget.currentWidget()
        return currentEditor.toPlainText()

    def __selectCancel(self):
        self.__GenerateSQLDialogView.reject()

    def __selectOK(self):
        self.__GenerateSQLDialogView.accept()
