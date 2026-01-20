import unittest
from unittest.mock import MagicMock

from app.controllers.ToolBarController import ToolBarController


class TestToolBarController(unittest.TestCase):
    def setUp(self):
        self.mockView = MagicMock()
        for actionName in [
            "actionCreateTable",
            "actionCreate_1_1_Rel",
            "actionCreate_1_n_Rel",
            "actionCreate_n_n_Rel",
            "actionCreateInheritance",
            "actionExportDiagram",
            "actionGenerateSQL",
        ]:
            action = MagicMock()
            action.triggered.connect = MagicMock()
            setattr(self.mockView, actionName, action)

        self.mockMenuBarController = MagicMock()
        self.controller = ToolBarController(self.mockView, self.mockMenuBarController)

    def testSignalsConnectedOnInit(self):
        self.mockView.actionCreateTable.triggered.connect.assert_called_once_with(
            self.controller._ToolBarController__selectCreateTableTool
        )
        self.mockView.actionCreate_1_1_Rel.triggered.connect.assert_called_once_with(
            self.controller._ToolBarController__selectCreate_1_1_RelTool
        )
        self.mockView.actionCreate_1_n_Rel.triggered.connect.assert_called_once_with(
            self.controller._ToolBarController__selectCreate_1_n_RelTool
        )
        self.mockView.actionCreate_n_n_Rel.triggered.connect.assert_called_once_with(
            self.controller._ToolBarController__selectCreate_n_n_RelTool
        )
        self.mockView.actionCreateInheritance.triggered.connect.assert_called_once_with(
            self.controller._ToolBarController__selectCreateInheritanceTool
        )
        self.mockView.actionExportDiagram.triggered.connect.assert_called_once_with(
            self.controller._ToolBarController__selectExportDiagramTool
        )
        self.mockView.actionGenerateSQL.triggered.connect.assert_called_once_with(
            self.controller._ToolBarController__selectGenerateSQLTool
        )

    def testSelectCreateTableToolDelegatesToMenuBarController(self):
        self.controller._ToolBarController__selectCreateTableTool()
        self.mockMenuBarController.selectCreateTableTool.assert_called_once_with()

    def testSelectCreate11RelToolDelegatesToMenuBarController(self):
        self.controller._ToolBarController__selectCreate_1_1_RelTool()
        self.mockMenuBarController.selectCreate_1_1_RelTool.assert_called_once_with()

    def testSelectCreateNNRelToolDelegatesToMenuBarController(self):
        self.controller._ToolBarController__selectCreate_n_n_RelTool()
        self.mockMenuBarController.selectCreate_n_n_RelTool.assert_called_once_with()

    def testSelectCreateInheritanceToolDelegatesToMenuBarController(self):
        self.controller._ToolBarController__selectCreateInheritanceTool()
        self.mockMenuBarController.selectCreateInheritanceTool.assert_called_once_with()

    def testSelectExportDiagramToolDelegatesToMenuBarController(self):
        self.controller._ToolBarController__selectExportDiagramTool()
        self.mockMenuBarController.selectExportDiagramTool.assert_called_once_with()

    def testSelectGenerateSQLToolDelegatesToMenuBarController(self):
        self.controller._ToolBarController__selectGenerateSQLTool()
        self.mockMenuBarController.selectGenerateSQLTool.assert_called_once_with()


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
