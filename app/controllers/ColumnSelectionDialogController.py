from app.views.ErrorDialogView import ErrorDialogView


class ColumnSelectionDialogController:
    def __init__(self, ColumnSelectionDialogView):
        self.__ColumnSelectionDialogView = ColumnSelectionDialogView
        self.__selectedColumnName = None
        self.__ColumnSelectionDialogView.cancelButton.clicked.connect(self.__selectCancel)
        self.__ColumnSelectionDialogView.okButton.clicked.connect(self.__selectOK)

    def __selectCancel(self):
        self.__ColumnSelectionDialogView.reject()

    def __selectOK(self):
        self.__selectedColumnName = self.__ColumnSelectionDialogView.columnSelectionComboBox.currentText()
        if self.__selectedColumnName:
            self.__ColumnSelectionDialogView.accept()
        else:
            dialogTitle = "ERROR"
            dialogText = f"Column Not Selected"
            ErrorDialog = ErrorDialogView(self.__ColumnSelectionDialogView, dialogTitle, dialogText)
            ErrorDialog.displayDialog()

    def getSelectedColumnName(self):
        return self.__selectedColumnName or None
