from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QRegularExpressionValidator


class OracleConnectionParamsDialogView(QDialog):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)
        self.__usernameRegex = QRegularExpression(r'^[A-Za-z_][A-Za-z0-9_]+$')
        self.__passwordRegex = QRegularExpression(r'^[^\s/]+$')
        self.__hostRegex = QRegularExpression(r'^[a-zA-Z0-9.-]+$')
        self.__portRegex = QRegularExpression(r'^(?:[1-9][0-9]{0,4}|6553[0-5]|[1-9][0-9]{0,3}|[0-9]{1,5})$')
        self.__serviceNameRegex = QRegularExpression(r'^[A-Za-z0-9._-]+$')

    def setupUI(self):
        if not self.objectName():
            self.setObjectName(u"OracleConnectionParamsDialog")
        self.resize(280, 180)
        self.setWindowTitle(u"Oracle Database Connection Parameters")

        self.__gridLayout = QGridLayout(self)

        self.__horizontalLayout = QHBoxLayout()
        self.__usernameLabel = QLabel(u"Username", self)
        self.__usernameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.usernameLineEdit = QLineEdit(self)
        usernameValidator = QRegularExpressionValidator(self.__usernameRegex, self.usernameLineEdit)
        self.usernameLineEdit.setValidator(usernameValidator)
        self.usernameLineEdit.setMaxLength(30)
        self.__horizontalLayout.addWidget(self.__usernameLabel)
        self.__horizontalLayout.addWidget(self.usernameLineEdit)
        self.__horizontalLayout.setStretch(0, 3)
        self.__horizontalLayout.setStretch(1, 7)
        self.__gridLayout.addLayout(self.__horizontalLayout, 0, 0, 1, 1)

        self.__horizontalLayout_2 = QHBoxLayout()
        self.__passwordLabel = QLabel(u"Password", self)
        self.__passwordLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.passwordLineEdit = QLineEdit(self)
        passwordValidator = QRegularExpressionValidator(self.__passwordRegex, self.passwordLineEdit)
        self.passwordLineEdit.setValidator(passwordValidator)
        self.passwordLineEdit.setMaxLength(128)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.__horizontalLayout_2.addWidget(self.__passwordLabel)
        self.__horizontalLayout_2.addWidget(self.passwordLineEdit)
        self.__horizontalLayout_2.setStretch(0, 3)
        self.__horizontalLayout_2.setStretch(1, 7)
        self.__gridLayout.addLayout(self.__horizontalLayout_2, 1, 0, 1, 1)

        self.__horizontalLayout_3 = QHBoxLayout()
        self.__hostLabel = QLabel(u"Host", self)
        self.__hostLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hostLineEdit = QLineEdit(self)
        hostValidator = QRegularExpressionValidator(self.__hostRegex, self.hostLineEdit)
        self.hostLineEdit.setValidator(hostValidator)
        self.hostLineEdit.setMaxLength(253)
        self.__horizontalLayout_3.addWidget(self.__hostLabel)
        self.__horizontalLayout_3.addWidget(self.hostLineEdit)
        self.__horizontalLayout_3.setStretch(0, 3)
        self.__horizontalLayout_3.setStretch(1, 7)
        self.__gridLayout.addLayout(self.__horizontalLayout_3, 2, 0, 1, 1)

        self.__horizontalLayout_4 = QHBoxLayout()
        self.__portLabel = QLabel(u"Port", self)
        self.__portLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.portLineEdit = QLineEdit(self)
        portValidator = QRegularExpressionValidator(self.__portRegex, self.portLineEdit)
        self.portLineEdit.setValidator(portValidator)
        self.portLineEdit.setMaxLength(5)
        self.__horizontalLayout_4.addWidget(self.__portLabel)
        self.__horizontalLayout_4.addWidget(self.portLineEdit)
        self.__horizontalLayout_4.setStretch(0, 3)
        self.__horizontalLayout_4.setStretch(1, 7)
        self.__gridLayout.addLayout(self.__horizontalLayout_4, 3, 0, 1, 1)

        self.__horizontalLayout_5 = QHBoxLayout()
        self.__serviceNameLabel = QLabel(u"Service Name", self)
        self.__serviceNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serviceNameLineEdit = QLineEdit(self)
        serviceNameValidator = QRegularExpressionValidator(self.__serviceNameRegex, self.serviceNameLineEdit)
        self.serviceNameLineEdit.setValidator(serviceNameValidator)
        self.serviceNameLineEdit.setMaxLength(128)
        self.__horizontalLayout_5.addWidget(self.__serviceNameLabel)
        self.__horizontalLayout_5.addWidget(self.serviceNameLineEdit)
        self.__horizontalLayout_5.setStretch(0, 3)
        self.__horizontalLayout_5.setStretch(1, 7)
        self.__gridLayout.addLayout(self.__horizontalLayout_5, 4, 0, 1, 1)

        self.__horizontalLayout_6 = QHBoxLayout()
        self.__horizontalLayout_7 = QHBoxLayout()
        self.cancelButton = QPushButton(u"Cancel", self)
        self.okButton = QPushButton(u"OK", self)
        self.__horizontalLayout_7.addWidget(self.cancelButton)
        self.__horizontalLayout_7.addWidget(self.okButton)
        self.__horizontalLayout_6.addLayout(self.__horizontalLayout_7)
        self.__gridLayout.addLayout(self.__horizontalLayout_6, 5, 0, 1, 1)

        self.__gridLayout.setRowStretch(0, 1)
        self.__gridLayout.setRowStretch(1, 1)
        self.__gridLayout.setRowStretch(2, 1)
        self.__gridLayout.setRowStretch(3, 1)
        self.__gridLayout.setRowStretch(4, 1)
        self.__gridLayout.setRowStretch(5, 1)

    def displayDialog(self):
        result = self.exec()
        return result
