class ExecutionSQLDialogController:
    def __init__(self, ExecutionSQLDialogView):
        self.__ExecutionSQLDialogView = ExecutionSQLDialogView

        self.__ExecutionSQLDialogView.cancelButton.clicked.connect(self.__selectCancel)
        self.__ExecutionSQLDialogView.okButton.clicked.connect(self.__selectOK)

    def __selectCancel(self):
        self.__ExecutionSQLDialogView.reject()

    def __selectOK(self):
        self.__ExecutionSQLDialogView.accept()
