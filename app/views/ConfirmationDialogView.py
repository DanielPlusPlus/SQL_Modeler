from PySide6.QtWidgets import QMessageBox


class ConfirmationDialogView(QMessageBox):
    def __init__(self, ParentWindow, title, text):
        super().__init__(ParentWindow)
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.No)

    def displayDialog(self):
        result = self.exec()
        return result == QMessageBox.StandardButton.Yes
