from app.views.ErrorDialogView import ErrorDialogView


class ColorChangeDialogController:
    def __init__(self, ColorChangeDialogView):
        self.__ColorChangeDialogView = ColorChangeDialogView
        self.__selectedColor = None
        self.__ColorChangeDialogView.cancelButton.clicked.connect(self.__selectCancel)
        self.__ColorChangeDialogView.okButton.clicked.connect(self.__selectOK)

    def __selectCancel(self):
        self.__ColorChangeDialogView.reject()

    def __selectOK(self):
        self.__selectedColor = self.__ColorChangeDialogView.currentColor()
        if self.__selectedColor.isValid():
            self.__ColorChangeDialogView.accept()
        else:
            dialogTitle = "ERROR"
            dialogText = f"Color is Not Valid"
            ErrorDialog = ErrorDialogView(self.__ColorChangeDialogView, dialogTitle, dialogText)
            ErrorDialog.displayDialog()

    def getSelectedColor(self):
        return self.__selectedColor
