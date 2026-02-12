from PySide6.QtWidgets import QDialog

from app.views.ColumnSelectionDialogView import ColumnSelectionDialogView
from app.views.ConfirmationDialogView import ConfirmationDialogView
from app.views.ErrorDialogView import ErrorDialogView
from app.views.RelationshipContextMenuView import RelationshipContextMenuView
from app.controllers.ConnectionsController import ConnectionsController
from app.controllers.ColumnSelectionDialogController import ColumnSelectionDialogController
from app.controllers.RelationshipContextMenuController import RelationshipContextMenuController
from app.enums.RelationshipContextMenuEnum import RelationshipContextMenuEnum


class RelationshipsController(ConnectionsController):
    def __init__(self, ParentWindow, RelationshipsView, RelationshipsModel, TablesModel):
        super().__init__(ParentWindow, TablesModel)
        self.__RelationshipsView = RelationshipsView
        self.__RelationshipsModel = RelationshipsModel
        self.__RelationshipContextMenuView = RelationshipContextMenuView(ParentWindow)
        self.__RelationshipContextMenuView.setupUI()
        self.__RelationshipContextMenuController = RelationshipContextMenuController(self.__RelationshipContextMenuView)
        self.__firstSelectedColumnName = None
        self.__secondSelectedColumnName = None
        self.__isFirstSelectedColumnPK = False
        self.__isSecondSelectedColumnPK = False
        self.__isRelationshipBeingDrawn = False
        self.__isContextMenuAtWork = False

    def setFirstSelectedColumnName(self):
        obtainedTableColumns = self._FirstClickedTable.getTableColumns()

        selectedColumnName = self.__displayColumnSelectionDialog(obtainedTableColumns)
        if selectedColumnName is None:
            return False
        self.__firstSelectedColumnName = selectedColumnName
        return True

    def setSecondSelectedColumnName(self):
        obtainedTableColumns = self._SecondClickedTable.getTableColumns()

        selectedColumnName = self.__displayColumnSelectionDialog(obtainedTableColumns)
        if selectedColumnName is None:
            return False
        self.__secondSelectedColumnName = selectedColumnName
        return True

    def __displayColumnSelectionDialog(self, obtainedTableColumns):
        ColumnSelectionDialog = ColumnSelectionDialogView(self._ParentWindow, obtainedTableColumns)
        ColumnSelectionDialog.setupUI()
        ColumnSelectionDialogControl = ColumnSelectionDialogController(ColumnSelectionDialog)
        if ColumnSelectionDialog.displayDialog() == QDialog.Accepted:
            return ColumnSelectionDialogControl.getSelectedColumnName()
        else:
            return None

    def __setForeignKeys(self):
        FirstTableColumnsModel = self._FirstClickedTable.getTableColumnsModel()
        SecondTableColumnsModel = self._SecondClickedTable.getTableColumnsModel()

        if not FirstTableColumnsModel.setForeignKeyByColumnName(self.__firstSelectedColumnName):
            self.__isFirstSelectedColumnPK = True
        if not SecondTableColumnsModel.setForeignKeyByColumnName(self.__secondSelectedColumnName):
            self.__isSecondSelectedColumnPK = True

    def __resetSelections(self):
        self.resetTables()
        self.__firstSelectedColumnName = None
        self.__secondSelectedColumnName = None
        self.__isFirstSelectedColumnPK = False
        self.__isSecondSelectedColumnPK = False

    def selectRelationshipBeingDrawn(self):
        self.__isRelationshipBeingDrawn = True

    def unselectRelationshipBeingDrawn(self):
        self.__isRelationshipBeingDrawn = False

    def getRelationshipBeingDrawnStatus(self):
        return self.__isRelationshipBeingDrawn

    def add_1_1_Relationship(self):
        self.__setForeignKeys()
        if self.__isFirstSelectedColumnPK and self.__isSecondSelectedColumnPK:
            self.__RelationshipsModel.add_1_1_Relationship(self._FirstClickedTable, self._SecondClickedTable,
                                                           self.__firstSelectedColumnName, self.__secondSelectedColumnName)
        else:
            self.displayWrongRelationshipDialog()
        self.__resetSelections()

    def add_1_n_Relationship(self):
        self.__setForeignKeys()
        if self.__isFirstSelectedColumnPK and not self.__isSecondSelectedColumnPK:
            self.__RelationshipsModel.add_1_n_Relationship(self._FirstClickedTable, self._SecondClickedTable,
                                                           self.__firstSelectedColumnName, self.__secondSelectedColumnName)
        else:
            self.displayWrongRelationshipDialog()
        self.__resetSelections()

    def add_n_n_Relationship(self):
        self.__setForeignKeys()
        if self.__isFirstSelectedColumnPK and self.__isSecondSelectedColumnPK:
            self.__RelationshipsModel.add_n_n_Relationship(self._FirstClickedTable, self._SecondClickedTable,
                                                           self.__firstSelectedColumnName, self.__secondSelectedColumnName)
        else:
            self.displayWrongRelationshipDialog()
        self.__resetSelections()

    def deleteRelationship(self, cursorPosition):
        ObtainedRelationship = self.__RelationshipsModel.getRelationshipFromPosition(cursorPosition)
        if ObtainedRelationship is not None:
            dialogTitle = "WARNING"
            dialogText = "Are you sure about deleting this relationship?"
            ConfirmationDialog = ConfirmationDialogView(self._ParentWindow, dialogTitle, dialogText)
            if ConfirmationDialog.displayDialog():
                self.__RelationshipsModel.deleteSelectedRelationship(ObtainedRelationship)

    def deleteRelationshipByTable(self, ObtainedTable):
        self.__RelationshipsModel.deleteSelectedRelationshipByTable(ObtainedTable)

    def selectDrawRelationshipBeingDrawn(self, cursorPosition):
        self.__RelationshipsView.drawRelationshipBeingDrawn(self._FirstClickedTable, cursorPosition)

    def selectDrawRelationships(self):
        self.__RelationshipsView.drawRelationships()

    def displayWrongRelationshipDialog(self):
        dialogTitle = "ERROR"
        dialogText = "You choose the wrong type of relationship"
        WrongRelationshipDialog = ErrorDialogView(self._ParentWindow, dialogTitle, dialogText)
        WrongRelationshipDialog.displayDialog()

    def displayRelationshipContextMenu(self, cursorPosition, globalCursorPosition):
        ObtainedRelationship = self.__RelationshipsModel.getRelationshipFromPosition(cursorPosition)
        if ObtainedRelationship is not None:
            self.__isContextMenuAtWork = True
            self.__RelationshipContextMenuView.exec(globalCursorPosition)
            if self.__RelationshipContextMenuController.getSelectDeleteRelationshipStatus():
                self.__RelationshipContextMenuController.unselectDeleteRelationship()
                self.__isContextMenuAtWork = False
                return RelationshipContextMenuEnum.DELETE
            return RelationshipContextMenuEnum.NONE

    def unselectContextMenuAtWork(self):
        self.__isContextMenuAtWork = False

    def getContextMenuAtWorkStatus(self):
        return self.__isContextMenuAtWork
