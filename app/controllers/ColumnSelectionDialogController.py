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
        self.__ColumnSelectionDialogView.accept()

    def getSelectedColumnName(self):
        return self.__selectedColumnName or None
