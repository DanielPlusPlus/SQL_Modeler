import unittest
from unittest.mock import patch, MagicMock
import oracledb

from app.controllers.OracleDatabaseController import OracleDatabaseController


class TestOracleDatabaseController(unittest.TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "pass"
        self.host = "localhost"
        self.port = "1521"
        self.serviceName = "xe"

    @patch("app.controllers.OracleDatabaseController.oracledb.connect")
    def testExecuteSQLCodeSuccess(self, mockConnect):
        mockConnection = MagicMock()
        mockCursor = MagicMock()
        mockConnect.return_value = mockConnection
        mockConnection.cursor.return_value.__enter__.return_value = mockCursor

        sqlCode = "SELECT 1 FROM dual; SELECT 2 FROM dual;"

        controller = OracleDatabaseController(
            self.username, self.password, self.host, self.port, self.serviceName
        )
        result = controller.executeSQLCode(sqlCode)

        expectedCalls = [
            unittest.mock.call("SELECT 1 FROM dual"),
            unittest.mock.call("SELECT 2 FROM dual"),
        ]
        mockCursor.execute.assert_has_calls(expectedCalls)

        mockConnection.commit.assert_called_once()
        mockConnection.close.assert_called_once()

        self.assertIn("Connected to Oracle database.", result)
        self.assertIn("Executed:\nSELECT 1 FROM dual", result)
        self.assertIn("Executed:\nSELECT 2 FROM dual", result)
        self.assertIn("All changes committed.", result)
        self.assertIn("Connection closed.", result)

    @patch("app.controllers.OracleDatabaseController.oracledb.connect")
    def testExecuteSQLCodeWithStatementError(self, mockConnect):
        mockConnection = MagicMock()
        mockCursor = MagicMock()
        mockConnect.return_value = mockConnection
        mockConnection.cursor.return_value.__enter__.return_value = mockCursor

        def executeSideEffect(stmt):
            if stmt == "BAD SQL":
                raise oracledb.DatabaseError("Syntax error")
            return None

        mockCursor.execute.side_effect = executeSideEffect

        sqlCode = "BAD SQL; SELECT 1 FROM dual;"

        controller = OracleDatabaseController(
            self.username, self.password, self.host, self.port, self.serviceName
        )
        result = controller.executeSQLCode(sqlCode)

        self.assertIn("ERROR in statement:\nBAD SQL\nSyntax error", result)
        self.assertIn("Executed:\nSELECT 1 FROM dual", result)
        self.assertIn("All changes committed.", result)
        self.assertIn("Connection closed.", result)

    @patch("app.controllers.OracleDatabaseController.oracledb.connect")
    def testExecuteSQLCodeConnectionError(self, mockConnect):
        mockConnect.side_effect = oracledb.Error("Connection failed")

        controller = OracleDatabaseController(
            self.username, self.password, self.host, self.port, self.serviceName
        )
        result = controller.executeSQLCode("SELECT 1 FROM dual;")

        self.assertIn("Connection or general error:\nConnection failed", result)


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
