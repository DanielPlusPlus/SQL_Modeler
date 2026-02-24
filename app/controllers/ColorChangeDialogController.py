from app.views.ErrorDialogView import ErrorDialogView


class ColorChangeDialogController:
    def __init__(self, ColorChangeDialogView, StructureModel):
        self.__ColorChangeDialogView = ColorChangeDialogView
        self.__StructureModel = StructureModel
        self.__ColorChangeDialogView.cancelButton.clicked.connect(self.__selectCancel)
        self.__ColorChangeDialogView.okButton.clicked.connect(self.__selectOK)

    def __selectCancel(self):
        self.__ColorChangeDialogView.reject()

    def __selectOK(self):
        if self.editStructureColor():
            self.__ColorChangeDialogView.accept()

    def editStructureColor(self):
        selectedColor = self.__ColorChangeDialogView.currentColor()
        if selectedColor.isValid():
            self.__StructureModel.changeColor(selectedColor)
            return True

        dialogTitle = "ERROR"
        dialogText = f"Color is Not Valid"
        ErrorDialog = ErrorDialogView(self.__ColorChangeDialogView, dialogTitle, dialogText)
        ErrorDialog.displayDialog()
        return False

