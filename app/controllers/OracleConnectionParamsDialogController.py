from app.views.ErrorDialogView import ErrorDialogView


class OracleConnectionParamsDialogController:
    def __init__(self, OracleConnectionsParamsView):
        self.__OracleConnectionsParamsView = OracleConnectionsParamsView
        self.username = None
        self.password = None
        self.host = None
        self.port = None
        self.serviceName = None
        self.__OracleConnectionsParamsView.cancelButton.clicked.connect(self.__selectCancel)
        self.__OracleConnectionsParamsView.okButton.clicked.connect(self.__selectOK)

    def __selectCancel(self):
        self.__OracleConnectionsParamsView.reject()

    def __selectOK(self):
        if self.__editConnectionParams():
            self.__OracleConnectionsParamsView.accept()

    def __editConnectionParams(self):
        self.username = self.__OracleConnectionsParamsView.usernameLineEdit.text()
        self.password = self.__OracleConnectionsParamsView.passwordLineEdit.text()
        self.host = self.__OracleConnectionsParamsView.hostLineEdit.text()
        self.port = int(self.__OracleConnectionsParamsView.portLineEdit.text())
        self.serviceName = self.__OracleConnectionsParamsView.serviceNameLineEdit.text()

        if self.username and self.password and self.port and self.serviceName:
            return True
        else:
            dialogText = f"Not All Fields are Filled"

        dialogTitle = "ERROR"
        ErrorDialog = ErrorDialogView(self.__OracleConnectionsParamsView, dialogTitle, dialogText)
        ErrorDialog.displayDialog()

        return False

    def getConnectionParams(self):
        return {
            "username": self.username,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "serviceName": self.serviceName
        }
