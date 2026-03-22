from typing import override

from app.views.ErrorDialogView import ErrorDialogView
from app.controllers.ConnectionParamsDialogController import ConnectionParamsDialogController


class MySQLConnectionParamsDialogController(ConnectionParamsDialogController):
    def __init__(self, OracleConnectionsParamsView):
        super().__init__(OracleConnectionsParamsView)
        self.__username = None
        self.__password = None
        self.__host = None
        self.__port = None
        self.__database = None

    @override
    def _editConnectionParams(self):
        self.__username = self._ConnectionsParamsView.usernameLineEdit.text()
        self.__password = self._ConnectionsParamsView.passwordLineEdit.text()
        self.__host = self._ConnectionsParamsView.hostLineEdit.text()
        self.__port = int(self._ConnectionsParamsView.portLineEdit.text())
        self.__database = self._ConnectionsParamsView.databaseLineEdit.text()

        if self.__username and self.__password and self.__port and self.__database:
            return True
        else:
            dialogText = f"Not All Fields are Filled"

        dialogTitle = "ERROR"
        ErrorDialog = ErrorDialogView(self._ConnectionsParamsView, dialogTitle, dialogText)
        ErrorDialog.displayDialog()

        return False

    @override
    def getConnectionParams(self):
        return {
            "username": self.__username,
            "password": self.__password,
            "host": self.__host,
            "port": self.__port,
            "database": self.__database
        }
