import unittest
from unittest.mock import MagicMock, patch, mock_open

from PySide6.QtWidgets import QDialog

from app.controllers.GenerateSQLDialogController import GenerateSQLDialogController


class TestGenerateSQLDialogController(unittest.TestCase):
    def setUp(self):
        self.parentWindow = MagicMock()
        self.mainWindowController = MagicMock()
        self.dialogView = MagicMock()
        self.dialogView.SQLCodeTextEdit.toPlainText.return_value = "SELECT * FROM users;"

        for btnName in ["copyCodeButton", "saveCodeButton", "testCodeButton", "cancelButton", "okButton"]:
            btn = MagicMock()
            btn.clicked.connect = MagicMock()
            setattr(self.dialogView, btnName, btn)

        self.controller = GenerateSQLDialogController(
            self.parentWindow,
            self.mainWindowController,
            self.dialogView
        )

    @patch("app.controllers.GenerateSQLDialogController.QGuiApplication")
    @patch("app.controllers.GenerateSQLDialogController.InfoDialogView")
    def testSelectCopyCodeCopiesToClipboardAndShowsInfoDialog(self, MockInfoDialogView, MockQGuiApp):
        mockClipboard = MagicMock()
        MockQGuiApp.clipboard.return_value = mockClipboard

        self.controller._GenerateSQLDialogController__selectCopyCode()

        mockClipboard.setText.assert_called_once_with("SELECT * FROM users;")
        MockInfoDialogView.assert_called_once()
        MockInfoDialogView.return_value.displayDialog.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("app.controllers.GenerateSQLDialogController.QFileDialog.getSaveFileName")
    @patch("app.controllers.GenerateSQLDialogController.InfoDialogView")
    def testSelectSaveCodeSavesFileSuccessfullyAndShowsInfoDialog(
        self, MockInfoDialogView, mockGetSaveFileName, mockFileOpen
    ):
        mockGetSaveFileName.return_value = ("output.sql", "sql")

        self.controller._GenerateSQLDialogController__selectSaveCode()

        mockFileOpen.assert_called_once_with("output.sql", "w", encoding="utf-8")
        mockFileOpen().write.assert_called_once_with("SELECT * FROM users;")
        MockInfoDialogView.return_value.displayDialog.assert_called_once()
        self.mainWindowController.selectCloseWithoutConfirmation.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("app.controllers.GenerateSQLDialogController.QFileDialog.getSaveFileName")
    @patch("app.controllers.GenerateSQLDialogController.ErrorDialogView")
    def testSelectSaveCodeHandlesFileWriteException(
        self, MockErrorDialogView, mockGetSaveFileName, mockFileOpen
    ):
        mockGetSaveFileName.return_value = ("output.sql", "sql")
        mockFileOpen.side_effect = Exception("Permission denied")

        self.controller._GenerateSQLDialogController__selectSaveCode()

        MockErrorDialogView.assert_called_once()
        MockErrorDialogView.return_value.displayDialog.assert_called_once()

    @patch("app.controllers.GenerateSQLDialogController.OracleConnectionDialogView")
    @patch("app.controllers.GenerateSQLDialogController.OracleDatabaseController")
    @patch("app.controllers.GenerateSQLDialogController.ExecutionSQLDialogView")
    @patch("app.controllers.GenerateSQLDialogController.ExecutionSQLDialogController")
    def testSelectTestCodeExecutesSqlAndShowsResult(
        self,
        MockExecSQLCtrl,
        MockExecSQLView,
        MockOracleDBCtrl,
        MockOracleConnDialog,
    ):
        MockOracleDBCtrl.return_value.executeSQLCode.return_value = "Executed successfully"

        mockConnDialogInstance = MagicMock()
        mockConnDialogInstance.exec.return_value = QDialog.Accepted
        mockConnDialogInstance.getConnectionParams.return_value = {
            "username": "u",
            "password": "p",
            "host": "h",
            "port": "1521",
            "serviceName": "xe",
        }
        MockOracleConnDialog.return_value = mockConnDialogInstance

        mockViewInstance = MagicMock()
        MockExecSQLView.return_value = mockViewInstance

        self.controller._GenerateSQLDialogController__selectTestCode()

        MockOracleConnDialog.assert_called_once_with(self.parentWindow)
        mockConnDialogInstance.exec.assert_called_once()

        MockOracleDBCtrl.assert_called_once_with("u", "p", "h", "1521", "xe")
        MockOracleDBCtrl.return_value.executeSQLCode.assert_called_once_with("SELECT * FROM users;")

        MockExecSQLView.assert_called_once_with(self.parentWindow)
        mockViewInstance.setupUI.assert_called_once_with("Executed successfully")
        MockExecSQLCtrl.assert_called_once_with(mockViewInstance)
        mockViewInstance.displayDialog.assert_called_once()

    @patch("app.controllers.GenerateSQLDialogController.OracleConnectionDialogView")
    @patch("app.controllers.GenerateSQLDialogController.ErrorDialogView")
    def testSelectTestCodeEmptySqlShowsErrorDialog(self, MockErrorDialogView, MockOracleConnDialog):
        self.dialogView.SQLCodeTextEdit.toPlainText.return_value = "   \n  "

        mockConnDialogInstance = MagicMock()
        mockConnDialogInstance.exec.return_value = QDialog.Accepted
        mockConnDialogInstance.getConnectionParams.return_value = {
            "username": "u",
            "password": "p",
            "host": "h",
            "port": "1521",
            "serviceName": "xe",
        }
        MockOracleConnDialog.return_value = mockConnDialogInstance

        self.controller._GenerateSQLDialogController__selectTestCode()

        MockOracleConnDialog.assert_called_once_with(self.parentWindow)
        mockConnDialogInstance.exec.assert_called_once()
        MockErrorDialogView.return_value.displayDialog.assert_called_once()

    def testSelectCancelCallsDialogReject(self):
        self.controller._GenerateSQLDialogController__selectCancel()
        self.dialogView.reject.assert_called_once()

    def testSelectOkCallsDialogAccept(self):
        self.controller._GenerateSQLDialogController__selectOK()
        self.dialogView.accept.assert_called_once()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
