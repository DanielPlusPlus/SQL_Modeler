from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QTextEdit


class ExecutionSQLDialogView(QDialog):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)

    def setupUI(self, executionResult):
        self.setObjectName(u"ExecuteSQLDialog")
        self.resize(600, 400)
        self.setWindowTitle(u"Execute SQL Code")

        self.__gridLayout = QGridLayout(self)

        self.__horizontalLayout = QHBoxLayout()
        self.__executeSQLCodeLabel = QLabel(u"Execution SQL Code Result", self)
        self.__executeSQLCodeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__horizontalLayout.addWidget(self.__executeSQLCodeLabel)
        self.__gridLayout.addLayout(self.__horizontalLayout, 0, 0, 1, 1)

        self.__horizontalLayout_2 = QHBoxLayout()
        self.__executionResultTextEdit = QTextEdit(self)
        font = QFont("Courier", 10)
        self.__executionResultTextEdit.setFont(font)
        self.__executionResultTextEdit.setReadOnly(True)
        self.__executionResultTextEdit.setPlainText(executionResult)
        self.__horizontalLayout_2.addWidget(self.__executionResultTextEdit)
        self.__gridLayout.addLayout(self.__horizontalLayout_2, 1, 0, 1, 1)

        self.__horizontalLayout_3 = QHBoxLayout()
        self.__horizontalLayout_4 = QHBoxLayout()
        self.__horizontalLayout_5 = QHBoxLayout()
        self.__horizontalLayout_6 = QHBoxLayout()
        self.__pleceholderWidget = QWidget(self)
        self.cancelButton = QPushButton(u"Cancel", self)
        self.okButton = QPushButton(u"OK", self)
        self.__horizontalLayout_4.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_5.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_6.addWidget(self.cancelButton)
        self.__horizontalLayout_6.addWidget(self.okButton)
        self.__horizontalLayout_3.addLayout(self.__horizontalLayout_5)
        self.__horizontalLayout_3.addLayout(self.__horizontalLayout_4)
        self.__horizontalLayout_3.addLayout(self.__horizontalLayout_6)
        self.__horizontalLayout_3.setStretch(0, 1)
        self.__horizontalLayout_3.setStretch(1, 1)
        self.__horizontalLayout_3.setStretch(2, 1)
        self.__gridLayout.addLayout(self.__horizontalLayout_3, 2, 0, 1, 1)

        self.__gridLayout.setRowStretch(0, 1)
        self.__gridLayout.setRowStretch(1, 17)
        self.__gridLayout.setRowStretch(2, 2)

    def displayDialog(self):
        result = self.exec()
        return result
