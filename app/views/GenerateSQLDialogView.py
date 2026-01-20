from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QLabel, QPushButton, QWidget

from app.views.widgets.CodeEditor import CodeEditor


class GenerateSQLDialogView(QDialog):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)

    def setupUI(self, SQLCode):
        self.setObjectName("GenerateSQLDialog")
        self.resize(600, 400)
        self.setWindowTitle("Generate SQL Code")

        self.__gridLayout = QGridLayout(self)

        self.__horizontalLayout = QHBoxLayout()
        self.__generateSQLCodeLabel = QLabel(u"Generated SQL Code", self)
        self.__generateSQLCodeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__horizontalLayout.addWidget(self.__generateSQLCodeLabel)
        self.__gridLayout.addLayout(self.__horizontalLayout, 0, 0, 1, 1)

        self.__horizontalLayout_2 = QHBoxLayout()
        self.SQLCodeTextEdit = CodeEditor(self)
        self.SQLCodeTextEdit.setReadOnly(True)
        self.SQLCodeTextEdit.setPlainText(SQLCode)
        self.__horizontalLayout_2.addWidget(self.SQLCodeTextEdit)
        self.__gridLayout.addLayout(self.__horizontalLayout_2, 1, 0, 1, 1)

        self.__horizontalLayout_3 = QHBoxLayout()
        self.copyCodeButton = QPushButton(u"Copy The Code", self)
        self.saveCodeButton = QPushButton(u"Save The Code", self)
        self.testCodeButton = QPushButton(u"Test The Code In Oracle", self)
        self.__horizontalLayout_3.addWidget(self.copyCodeButton)
        self.__horizontalLayout_3.addWidget(self.saveCodeButton)
        self.__horizontalLayout_3.addWidget(self.testCodeButton)
        self.__horizontalLayout_3.setStretch(0, 1)
        self.__horizontalLayout_3.setStretch(1, 1)
        self.__horizontalLayout_3.setStretch(2, 1)
        self.__gridLayout.addLayout(self.__horizontalLayout_3, 2, 0, 1, 1)

        self.__horizontalLayout_4 = QHBoxLayout()
        self.__horizontalLayout_5 = QHBoxLayout()
        self.__horizontalLayout_6 = QHBoxLayout()
        self.__horizontalLayout_7 = QHBoxLayout()
        self.__pleceholderWidget = QWidget(self)
        self.cancelButton = QPushButton(u"Cancel", self)
        self.okButton = QPushButton(u"OK", self)
        self.__horizontalLayout_6.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_5.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_7.addWidget(self.cancelButton)
        self.__horizontalLayout_7.addWidget(self.okButton)
        self.__horizontalLayout_4.addLayout(self.__horizontalLayout_6)
        self.__horizontalLayout_4.addLayout(self.__horizontalLayout_5)
        self.__horizontalLayout_4.addLayout(self.__horizontalLayout_7)
        self.__horizontalLayout_4.setStretch(0, 1)
        self.__horizontalLayout_4.setStretch(1, 1)
        self.__horizontalLayout_4.setStretch(2, 1)
        self.__gridLayout.addLayout(self.__horizontalLayout_4, 3, 0, 1, 1)

        self.__gridLayout.setRowStretch(0, 1)
        self.__gridLayout.setRowStretch(1, 15)
        self.__gridLayout.setRowStretch(2, 2)
        self.__gridLayout.setRowStretch(3, 2)

    def displayDialog(self):
        result = self.exec()
        return result



