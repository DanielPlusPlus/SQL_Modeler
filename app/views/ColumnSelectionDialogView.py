from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox


class ColumnSelectionDialogView(QDialog):
    def __init__(self, ParentWindow, ObtainedTableColumns):
        super().__init__(ParentWindow)
        self.setWindowTitle("Select Column")
        self.__selected_column = None

        layout = QVBoxLayout(self)

        label = QLabel("Select column:")
        layout.addWidget(label)

        self.__combo_box = QComboBox()
        self.__combo_box.addItems([col["columnName"] for col in ObtainedTableColumns])
        layout.addWidget(self.__combo_box)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def displayDialog(self):
        if self.exec() == QDialog.Accepted:
            return self.__combo_box.currentText() or None
        return None
