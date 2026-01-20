from PySide6.QtWidgets import QMessageBox


class InfoDialogView(QMessageBox):
    def __init__(self, ParentWindow, title, text):
        super().__init__(ParentWindow)
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QMessageBox.Icon.Information)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setDefaultButton(QMessageBox.StandardButton.Ok)

    def displayDialog(self):
        result = self.exec()
        return result == QMessageBox.StandardButton.Ok
