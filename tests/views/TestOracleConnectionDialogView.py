import sys
import unittest

from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton

from app.views.OracleConnectionParamsDialogView import OracleConnectionDialogView

app = QApplication.instance() or QApplication(sys.argv)


class TestOracleConnectionDialogView(unittest.TestCase):
    def setUp(self):
        self.dialog = OracleConnectionDialogView()

    def test_dialog_title_and_type(self):
        self.assertEqual(self.dialog.windowTitle(), "Oracle Connection Parameters")
        self.assertTrue(isinstance(self.dialog, type(self.dialog)))

    def test_widgets_exist_and_types(self):
        self.assertIsInstance(self.dialog.usernameInput, QLineEdit)
        self.assertIsInstance(self.dialog.passwordInput, QLineEdit)
        self.assertIsInstance(self.dialog.hostInput, QLineEdit)
        self.assertIsInstance(self.dialog.portInput, QLineEdit)
        self.assertIsInstance(self.dialog.serviceNameInput, QLineEdit)
        self.assertIsInstance(self.dialog.okButton, QPushButton)
        self.assertIsInstance(self.dialog.cancelButton, QPushButton)

    def test_placeholders_and_echo_mode(self):
        self.assertEqual(self.dialog.usernameInput.placeholderText(), "Username")
        self.assertEqual(self.dialog.passwordInput.placeholderText(), "Password")
        self.assertEqual(self.dialog.passwordInput.echoMode(), QLineEdit.Password)
        self.assertEqual(self.dialog.hostInput.placeholderText(), "Host")
        self.assertEqual(self.dialog.portInput.placeholderText(), "Port")
        self.assertEqual(self.dialog.serviceNameInput.placeholderText(), "Service Name")

    def test_get_connection_params_with_values(self):
        self.dialog.usernameInput.setText("user1")
        self.dialog.passwordInput.setText("pass1")
        self.dialog.hostInput.setText("localhost")
        self.dialog.portInput.setText("1522")
        self.dialog.serviceNameInput.setText("orclpdb1")

        params = self.dialog.getConnectionParams()

        self.assertEqual(params["username"], "user1")
        self.assertEqual(params["password"], "pass1")
        self.assertEqual(params["host"], "localhost")
        self.assertEqual(params["port"], 1522)
        self.assertEqual(params["serviceName"], "orclpdb1")

    def test_get_connection_params_default_port_when_empty(self):
        self.dialog.usernameInput.setText("user2")
        self.dialog.passwordInput.setText("pass2")
        self.dialog.hostInput.setText("192.168.0.1")
        self.dialog.portInput.setText("")
        self.dialog.serviceNameInput.setText("XE")

        params = self.dialog.getConnectionParams()

        self.assertEqual(params["username"], "user2")
        self.assertEqual(params["password"], "pass2")
        self.assertEqual(params["host"], "192.168.0.1")
        self.assertEqual(params["port"], 1521)
        self.assertEqual(params["serviceName"], "XE")

    def test_buttons_text(self):
        self.assertEqual(self.dialog.okButton.text(), "OK")
        self.assertEqual(self.dialog.cancelButton.text(), "Cancel")


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)