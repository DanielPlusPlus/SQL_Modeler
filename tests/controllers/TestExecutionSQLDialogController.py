import unittest
from unittest.mock import MagicMock

from app.controllers.ExecutionSQLDialogController import ExecutionSQLDialogController


class TestExecutionDialogController(unittest.TestCase):

    def setUp(self):
        self.mockExecutionSqlDialogView = MagicMock()
        self.mockCancelButton = MagicMock()
        self.mockOkButton = MagicMock()

        self.mockExecutionSqlDialogView.cancelButton = self.mockCancelButton
        self.mockExecutionSqlDialogView.okButton = self.mockOkButton

        self.controller = ExecutionSQLDialogController(self.mockExecutionSqlDialogView)

    def testConstructorBindsButtons(self):
        self.mockCancelButton.clicked.connect.assert_called_once_with(
            self.controller._ExecutionSQLDialogController__selectCancel
        )
        self.mockOkButton.clicked.connect.assert_called_once_with(
            self.controller._ExecutionSQLDialogController__selectOK
        )

    def testSelectCancelCallsReject(self):
        self.controller._ExecutionSQLDialogController__selectCancel()
        self.mockExecutionSqlDialogView.reject.assert_called_once()

    def testSelectOkCallsAccept(self):
        self.controller._ExecutionSQLDialogController__selectOK()
        self.mockExecutionSqlDialogView.accept.assert_called_once()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
