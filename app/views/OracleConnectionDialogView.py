from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt


class OracleConnectionDialogView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Oracle Connection Parameters")

        self.usernameInput = QLineEdit(self)
        self.usernameInput.setPlaceholderText("Username")

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setPlaceholderText("Password")
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.hostInput = QLineEdit(self)
        self.hostInput.setPlaceholderText("Host")

        self.portInput = QLineEdit(self)
        self.portInput.setPlaceholderText("Port")

        self.serviceNameInput = QLineEdit(self)
        self.serviceNameInput.setPlaceholderText("Service Name")

        self.okButton = QPushButton("OK", self)
        self.cancelButton = QPushButton("Cancel", self)

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Enter Oracle Database Connection Parameters"))
        layout.addWidget(self.usernameInput)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.hostInput)
        layout.addWidget(self.portInput)
        layout.addWidget(self.serviceNameInput)
        layout.addWidget(self.okButton)
        layout.addWidget(self.cancelButton)

    def getConnectionParams(self):
        return {
            "username": self.usernameInput.text(),
            "password": self.passwordInput.text(),
            "host": self.hostInput.text(),
            "port": int(self.portInput.text()) if self.portInput.text() else 1521,
            "serviceName": self.serviceNameInput.text()
        }
