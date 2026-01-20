import unittest
from unittest.mock import MagicMock, patch

from app.controllers.RelationshipsController import RelationshipsController
from app.enums.RelationshipContextMenuEnum import RelationshipContextMenuEnum


class TestRelationshipsController(unittest.TestCase):

    @patch("app.controllers.RelationshipsController.RelationshipContextMenuView")
    @patch("app.controllers.RelationshipsController.RelationshipContextMenuController")
    def setUp(self, MockContextMenuController, MockContextMenuView):
        self.mockParentWindow = MagicMock()
        self.mockRelationshipsView = MagicMock()
        self.mockRelationshipsModel = MagicMock()
        self.mockTablesModel = MagicMock()

        self.mockContextMenuView = MockContextMenuView.return_value
        self.mockContextMenuController = MockContextMenuController.return_value

        self.controller = RelationshipsController(
            self.mockParentWindow,
            self.mockRelationshipsView,
            self.mockRelationshipsModel,
            self.mockTablesModel
        )

    @patch("app.controllers.RelationshipsController.ColumnSelectionDialogView")
    def testSetFirstSelectedColumnName_success(self, MockColumnSelectionDialog):
        mockTable = MagicMock()
        mockTable.getTableColumns.return_value = ["col1", "col2"]
        self.controller._FirstClickedTable = mockTable

        dialog_instance = MockColumnSelectionDialog.return_value
        dialog_instance.displayDialog.return_value = "col1"

        result = self.controller.setFirstSelectedColumnName()

        self.assertTrue(result)
        self.assertEqual(
            self.controller._RelationshipsController__firstSelectedColumnName,
            "col1"
        )
        MockColumnSelectionDialog.assert_called_once_with(self.mockParentWindow, ["col1", "col2"])
        dialog_instance.displayDialog.assert_called_once()

    @patch("app.controllers.RelationshipsController.ColumnSelectionDialogView")
    def testSetFirstSelectedColumnName_cancel(self, MockColumnSelectionDialog):
        mockTable = MagicMock()
        mockTable.getTableColumns.return_value = ["col1", "col2"]
        self.controller._FirstClickedTable = mockTable

        dialog_instance = MockColumnSelectionDialog.return_value
        dialog_instance.displayDialog.return_value = None

        result = self.controller.setFirstSelectedColumnName()

        self.assertFalse(result)
        self.assertIsNone(self.controller._RelationshipsController__firstSelectedColumnName)

    @patch("app.controllers.RelationshipsController.ColumnSelectionDialogView")
    def testSetSecondSelectedColumnName_success(self, MockColumnSelectionDialog):
        mockTable = MagicMock()
        mockTable.getTableColumns.return_value = ["c1", "c2"]
        self.controller._SecondClickedTable = mockTable

        dialog_instance = MockColumnSelectionDialog.return_value
        dialog_instance.displayDialog.return_value = "c2"

        result = self.controller.setSecondSelectedColumnName()

        self.assertTrue(result)
        self.assertEqual(
            self.controller._RelationshipsController__secondSelectedColumnName,
            "c2"
        )
        MockColumnSelectionDialog.assert_called_once_with(self.mockParentWindow, ["c1", "c2"])
        dialog_instance.displayDialog.assert_called_once()

    @patch("app.controllers.RelationshipsController.ColumnSelectionDialogView")
    def testSetSecondSelectedColumnName_cancel(self, MockColumnSelectionDialog):
        mockTable = MagicMock()
        mockTable.getTableColumns.return_value = ["c1", "c2"]
        self.controller._SecondClickedTable = mockTable

        dialog_instance = MockColumnSelectionDialog.return_value
        dialog_instance.displayDialog.return_value = None

        result = self.controller.setSecondSelectedColumnName()

        self.assertFalse(result)
        self.assertIsNone(self.controller._RelationshipsController__secondSelectedColumnName)

    def _prepare_tables_and_columns_models(self, first_fk_ok, second_fk_ok):
        first_table = MagicMock()
        second_table = MagicMock()
        first_columns_model = MagicMock()
        second_columns_model = MagicMock()

        first_table.getTableColumnsModel.return_value = first_columns_model
        second_table.getTableColumnsModel.return_value = second_columns_model

        first_columns_model.setForeignKeyByColumnName.return_value = first_fk_ok
        second_columns_model.setForeignKeyByColumnName.return_value = second_fk_ok

        self.controller._FirstClickedTable = first_table
        self.controller._SecondClickedTable = second_table
        self.controller._RelationshipsController__firstSelectedColumnName = "colA"
        self.controller._RelationshipsController__secondSelectedColumnName = "colB"

        self.controller.resetTables = MagicMock()

        return first_table, second_table, first_columns_model, second_columns_model

    @patch("app.controllers.RelationshipsController.ErrorDialogView")
    def testAdd11Relationship_bothPK_addsRelationship(self, MockErrorDialogView):
        first_table, second_table, _, _ = self._prepare_tables_and_columns_models(
            first_fk_ok=False, second_fk_ok=False
        )

        self.controller.add_1_1_Relationship()

        self.mockRelationshipsModel.add_1_1_Relationship.assert_called_once_with(
            first_table, second_table, "colA", "colB"
        )
        self.controller.resetTables.assert_called_once()
        MockErrorDialogView.assert_not_called()
        self.assertIsNone(self.controller._RelationshipsController__firstSelectedColumnName)
        self.assertIsNone(self.controller._RelationshipsController__secondSelectedColumnName)

    @patch("app.controllers.RelationshipsController.ErrorDialogView")
    def testAdd11Relationship_wrongTypes_showsError(self, MockErrorDialogView):
        self._prepare_tables_and_columns_models(first_fk_ok=True, second_fk_ok=False)

        self.controller.add_1_1_Relationship()

        self.mockRelationshipsModel.add_1_1_Relationship.assert_not_called()
        MockErrorDialogView.assert_called_once()
        MockErrorDialogView.return_value.displayDialog.assert_called_once()
        self.controller.resetTables.assert_called_once()

    @patch("app.controllers.RelationshipsController.ErrorDialogView")
    def testAdd1NRelationship_correctTypes_addsRelationship(self, MockErrorDialogView):
        first_table, second_table, _, _ = self._prepare_tables_and_columns_models(
            first_fk_ok=False, second_fk_ok=True
        )

        self.controller.add_1_n_Relationship()

        self.mockRelationshipsModel.add_1_n_Relationship.assert_called_once_with(
            first_table, second_table, "colA", "colB"
        )
        self.controller.resetTables.assert_called_once()
        MockErrorDialogView.assert_not_called()

    @patch("app.controllers.RelationshipsController.ErrorDialogView")
    def testAdd1NRelationship_wrongTypes_showsError(self, MockErrorDialogView):
        self._prepare_tables_and_columns_models(first_fk_ok=False, second_fk_ok=False)

        self.controller.add_1_n_Relationship()

        self.mockRelationshipsModel.add_1_n_Relationship.assert_not_called()
        MockErrorDialogView.assert_called_once()
        MockErrorDialogView.return_value.displayDialog.assert_called_once()
        self.controller.resetTables.assert_called_once()

    @patch("app.controllers.RelationshipsController.ErrorDialogView")
    def testAddNNRelationship_correctTypes_addsRelationship(self, MockErrorDialogView):
        first_table, second_table, _, _ = self._prepare_tables_and_columns_models(
            first_fk_ok=True, second_fk_ok=True
        )

        self.controller.add_n_n_Relationship()

        self.mockRelationshipsModel.add_n_n_Relationship.assert_called_once_with(
            first_table, second_table, "colA", "colB"
        )
        self.controller.resetTables.assert_called_once()
        MockErrorDialogView.assert_not_called()

    @patch("app.controllers.RelationshipsController.ErrorDialogView")
    def testAddNNRelationship_wrongTypes_showsError(self, MockErrorDialogView):
        self._prepare_tables_and_columns_models(first_fk_ok=False, second_fk_ok=True)

        self.controller.add_n_n_Relationship()

        self.mockRelationshipsModel.add_n_n_Relationship.assert_not_called()
        MockErrorDialogView.assert_called_once()
        MockErrorDialogView.return_value.displayDialog.assert_called_once()
        self.controller.resetTables.assert_called_once()

    def testSelectAndUnselectRelationshipBeingDrawn(self):
        self.assertFalse(self.controller.getRelationshipBeingDrawnStatus())
        self.controller.selectRelationshipBeingDrawn()
        self.assertTrue(self.controller.getRelationshipBeingDrawnStatus())
        self.controller.unselectRelationshipBeingDrawn()
        self.assertFalse(self.controller.getRelationshipBeingDrawnStatus())

    @patch("app.controllers.RelationshipsController.ConfirmationDialogView")
    def testDeleteRelationshipWithConfirmation(self, MockConfirmationDialog):
        cursorPos = (10, 20)
        mockRel = MagicMock()
        self.mockRelationshipsModel.getRelationshipFromPosition.return_value = mockRel

        instance = MockConfirmationDialog.return_value
        instance.displayDialog.return_value = True

        self.controller.deleteRelationship(cursorPos)

        self.mockRelationshipsModel.deleteSelectedRelationship.assert_called_once_with(mockRel)
        instance.displayDialog.assert_called_once()

    @patch("app.controllers.RelationshipsController.ConfirmationDialogView")
    def testDeleteRelationshipCancelled(self, MockConfirmationDialog):
        cursorPos = (10, 20)
        mockRel = MagicMock()
        self.mockRelationshipsModel.getRelationshipFromPosition.return_value = mockRel

        instance = MockConfirmationDialog.return_value
        instance.displayDialog.return_value = False

        self.controller.deleteRelationship(cursorPos)

        self.mockRelationshipsModel.deleteSelectedRelationship.assert_not_called()
        instance.displayDialog.assert_called_once()

    def testDeleteRelationshipNone(self):
        cursorPos = (10, 20)
        self.mockRelationshipsModel.getRelationshipFromPosition.return_value = None

        self.controller.deleteRelationship(cursorPos)

        self.mockRelationshipsModel.deleteSelectedRelationship.assert_not_called()

    def testDeleteRelationshipByTable_callsModel(self):
        mockTable = MagicMock()
        self.controller.deleteRelationshipByTable(mockTable)
        self.mockRelationshipsModel.deleteSelectedRelationshipByTable.assert_called_once_with(mockTable)

    def testSelectDrawRelationshipBeingDrawn(self):
        first_table = MagicMock()
        self.controller._FirstClickedTable = first_table
        cursorPos = (10, 20)

        self.controller.selectDrawRelationshipBeingDrawn(cursorPos)

        self.mockRelationshipsView.drawRelationshipBeingDrawn.assert_called_once_with(first_table, cursorPos)

    def testSelectDrawRelationships(self):
        self.controller.selectDrawRelationships()
        self.mockRelationshipsView.drawRelationships.assert_called_once()

    @patch("app.controllers.RelationshipsController.ErrorDialogView")
    def testDisplayWrongRelationshipDialog(self, MockErrorDialogView):
        self.controller.displayWrongRelationshipDialog()
        MockErrorDialogView.assert_called_once_with(
            self.mockParentWindow,
            "ERROR",
            "You choose the wrong type of relationship"
        )
        MockErrorDialogView.return_value.displayDialog.assert_called_once()

    def testDisplayRelationshipContextMenu_delete(self):
        cursorPos = (10, 20)
        globalPos = (100, 200)
        mockRel = MagicMock()
        self.mockRelationshipsModel.getRelationshipFromPosition.return_value = mockRel
        self.mockContextMenuController.getSelectDeleteRelationshipStatus.return_value = True

        result = self.controller.displayRelationshipContextMenu(cursorPos, globalPos)

        self.mockContextMenuView.exec.assert_called_once_with(globalPos)
        self.mockContextMenuController.unselectDeleteRelationship.assert_called_once()
        self.assertEqual(result, RelationshipContextMenuEnum.DELETE)
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())

    def testDisplayRelationshipContextMenu_none(self):
        cursorPos = (10, 20)
        globalPos = (100, 200)
        mockRel = MagicMock()
        self.mockRelationshipsModel.getRelationshipFromPosition.return_value = mockRel
        self.mockContextMenuController.getSelectDeleteRelationshipStatus.return_value = False

        result = self.controller.displayRelationshipContextMenu(cursorPos, globalPos)

        self.mockContextMenuView.exec.assert_called_once_with(globalPos)
        self.assertEqual(result, RelationshipContextMenuEnum.NONE)
        self.assertTrue(self.controller.getContextMenuAtWorkStatus())

    def testDisplayRelationshipContextMenu_noRelationship(self):
        cursorPos = (10, 20)
        globalPos = (100, 200)
        self.mockRelationshipsModel.getRelationshipFromPosition.return_value = None

        result = self.controller.displayRelationshipContextMenu(cursorPos, globalPos)

        self.assertIsNone(result)
        self.mockContextMenuView.exec.assert_not_called()

    def testContextMenuAtWorkStatusMethods(self):
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())
        self.controller.unselectContextMenuAtWork()
        self.assertFalse(self.controller.getContextMenuAtWorkStatus())


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
