import unittest
from unittest.mock import MagicMock

from app.controllers.MenuBarController import MenuBarController
from app.enums.ConnectionsStatusEnum import ConnectionsStatusEnum


class DummyAction:
    def __init__(self):
        self.triggered = MagicMock()


class DummyMenuBarView:
    def __init__(self):
        self.actionImportSQL = DummyAction()
        self.actionExportDiagram = DummyAction()
        self.actionGenerateSQL = DummyAction()
        self.actionQuit = DummyAction()
        self.actionCreateTable = DummyAction()
        self.actionCreate_1_1_Rel = DummyAction()
        self.actionCreate_1_n_Rel = DummyAction()
        self.actionCreate_n_n_Rel = DummyAction()
        self.actionCreateInheritance = DummyAction()


class TestMenuBarController(unittest.TestCase):
    def setUp(self):
        self.menuBarView = DummyMenuBarView()
        self.mainWindowController = MagicMock()
        self.drawingAreaController = MagicMock()
        self.loadSQLController = MagicMock()
        self.exportDiagramController = MagicMock()
        self.generateSQLController = MagicMock()

        for action in [
            self.menuBarView.actionImportSQL,
            self.menuBarView.actionExportDiagram,
            self.menuBarView.actionGenerateSQL,
            self.menuBarView.actionQuit,
            self.menuBarView.actionCreateTable,
            self.menuBarView.actionCreate_1_1_Rel,
            self.menuBarView.actionCreate_1_n_Rel,
            self.menuBarView.actionCreate_n_n_Rel,
            self.menuBarView.actionCreateInheritance,
        ]:
            action.triggered.connect = MagicMock()

        self.controller = MenuBarController(
            self.menuBarView,
            self.mainWindowController,
            self.drawingAreaController,
            self.loadSQLController,
            self.exportDiagramController,
            self.generateSQLController,
        )

    def test_actions_connected(self):
        self.menuBarView.actionImportSQL.triggered.connect.assert_called_once()
        self.menuBarView.actionExportDiagram.triggered.connect.assert_called_once()
        self.menuBarView.actionGenerateSQL.triggered.connect.assert_called_once()
        self.menuBarView.actionQuit.triggered.connect.assert_called_once()
        self.menuBarView.actionCreateTable.triggered.connect.assert_called_once()
        self.menuBarView.actionCreate_1_1_Rel.triggered.connect.assert_called_once()
        self.menuBarView.actionCreate_1_n_Rel.triggered.connect.assert_called_once()
        self.menuBarView.actionCreate_n_n_Rel.triggered.connect.assert_called_once()
        self.menuBarView.actionCreateInheritance.triggered.connect.assert_called_once()

    def test_select_import_sql_calls_controller(self):
        self.controller._MenuBarController__selectImportSQL()
        self.loadSQLController.openFileDialogAndProcessSQL.assert_called_once()

    def test_select_export_diagram_tool(self):
        self.controller.selectExportDiagramTool()
        self.drawingAreaController.unselectConnectionsBeingDrawn.assert_called_once()
        self.drawingAreaController.updateView.assert_called_once()
        self.exportDiagramController.exportDiagramToPNG.assert_called_once()

    def test_select_generate_sql_tool(self):
        self.controller.selectGenerateSQLTool()
        self.drawingAreaController.unselectConnectionsBeingDrawn.assert_called_once()
        self.drawingAreaController.updateView.assert_called_once()
        self.generateSQLController.displayDialog.assert_called_once()

    def test_select_quit_calls_main_window_close(self):
        self.controller._MenuBarController__selectQuit()
        self.mainWindowController.closeWindow.assert_called_once()

    def test_select_create_table_tool_sets_flag_and_unselects_others(self):
        self.controller.selectCreate_1_1_RelTool()
        self.controller.selectCreateTableTool()
        self.assertTrue(self.controller.getCreateTableToolStatus())
        self.assertEqual(self.controller.getCreate_1_1_RelToolStatus(), ConnectionsStatusEnum.NOT_IN_MOTION)

    def test_unselect_create_table_tool(self):
        self.controller.selectCreateTableTool()
        self.controller.unselectCreateTableTool()
        self.assertFalse(self.controller.getCreateTableToolStatus())

    def test_select_create_1_1_rel_tool_and_status_changes(self):
        self.controller.selectCreate_1_1_RelTool()
        self.assertEqual(
            self.controller.getCreate_1_1_RelToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK,
        )
        self.controller.changeStatusToAfterClick_1_1_RelTool()
        self.assertEqual(
            self.controller.getCreate_1_1_RelToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK,
        )
        self.controller.unselectCreate_1_1_RelTool()
        self.assertEqual(
            self.controller.getCreate_1_1_RelToolStatus(),
            ConnectionsStatusEnum.NOT_IN_MOTION,
        )

    def test_select_create_1_n_rel_tool_and_status_changes(self):
        self.controller.selectCreate_1_n_RelTool()
        self.assertEqual(
            self.controller.getCreate_1_n_RelToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK,
        )
        self.controller.changeStatusToAfterClick_1_n_RelTool()
        self.assertEqual(
            self.controller.getCreate_1_n_RelToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK,
        )
        self.controller.unselectCreate_1_n_RelTool()
        self.assertEqual(
            self.controller.getCreate_1_n_RelToolStatus(),
            ConnectionsStatusEnum.NOT_IN_MOTION,
        )

    def test_select_create_n_n_rel_tool_and_status_changes(self):
        self.controller.selectCreate_n_n_RelTool()
        self.assertEqual(
            self.controller.getCreate_n_n_RelToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK,
        )
        self.controller.changeStatusToAfterClick_n_n_RelTool()
        self.assertEqual(
            self.controller.getCreate_n_n_RelToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK,
        )
        self.controller.unselectCreate_n_n_RelTool()
        self.assertEqual(
            self.controller.getCreate_n_n_RelToolStatus(),
            ConnectionsStatusEnum.NOT_IN_MOTION,
        )

    def test_select_create_inheritance_tool_and_status_changes(self):
        self.controller.selectCreateInheritanceTool()
        self.assertEqual(
            self.controller.getCreateInheritanceToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK,
        )
        self.controller.changeStatusToAfterClickInheritanceTool()
        self.assertEqual(
            self.controller.getCreateInheritanceToolStatus(),
            ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK,
        )
        self.controller.unselectCreateInheritanceTool()
        self.assertEqual(
            self.controller.getCreateInheritanceToolStatus(),
            ConnectionsStatusEnum.NOT_IN_MOTION,
        )

    def test_unselect_all_tools_resets_flags(self):
        self.controller.selectCreateTableTool()
        self.controller.selectCreate_1_1_RelTool()
        self.controller.selectCreate_1_n_RelTool()
        self.controller.selectCreate_n_n_RelTool()
        self.controller.selectCreateInheritanceTool()

        self.controller._MenuBarController__unselectAllTools()

        self.assertFalse(self.controller.getCreateTableToolStatus())
        self.assertEqual(self.controller.getCreate_1_1_RelToolStatus(), ConnectionsStatusEnum.NOT_IN_MOTION)
        self.assertEqual(self.controller.getCreate_1_n_RelToolStatus(), ConnectionsStatusEnum.NOT_IN_MOTION)
        self.assertEqual(self.controller.getCreate_n_n_RelToolStatus(), ConnectionsStatusEnum.NOT_IN_MOTION)
        self.assertEqual(self.controller.getCreateInheritanceToolStatus(), ConnectionsStatusEnum.NOT_IN_MOTION)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
