from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QLabel, QComboBox, QPushButton


class ColumnSelectionDialogView(QDialog):
    def __init__(self, ParentWindow, ObtainedTableColumns):
        super().__init__(ParentWindow)
        self.__ObtainedTableColumns = ObtainedTableColumns

    def setupUI(self):
        if not self.objectName():
            self.setObjectName(u"ColumnSelectionSQLDialog")
        self.setWindowTitle(u"Select Column")

        self.__gridLayout = QGridLayout(self)

        self.__horizontalLayout = QHBoxLayout()
        self.__selectColumnLabel = QLabel(u"Select Column", self)
        self.__selectColumnLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__horizontalLayout.addWidget(self.__selectColumnLabel)
        self.__gridLayout.addLayout(self.__horizontalLayout, 0, 0, 1, 1)

        self.__horizontalLayout_2 = QHBoxLayout()
        self.columnSelectionComboBox = QComboBox()
        self.columnSelectionComboBox.addItems([col["columnName"] for col in self.__ObtainedTableColumns])
        self.__horizontalLayout_2.addWidget(self.columnSelectionComboBox)
        self.__gridLayout.addLayout(self.__horizontalLayout_2, 1, 0, 1, 1)

        self.__horizontalLayout_3 = QHBoxLayout()
        self.__horizontalLayout_4 = QHBoxLayout()
        self.cancelButton = QPushButton(u"Cancel", self)
        self.okButton = QPushButton(u"OK", self)
        self.__horizontalLayout_4.addWidget(self.cancelButton)
        self.__horizontalLayout_4.addWidget(self.okButton)
        self.__horizontalLayout_3.addLayout(self.__horizontalLayout_4)
        self.__gridLayout.addLayout(self.__horizontalLayout_3, 2, 0, 1, 1)

    def displayDialog(self):
        result = self.exec()
        return result
