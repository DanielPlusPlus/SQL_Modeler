from app.views.ConfirmationDialogView import ConfirmationDialogView
from app.views.TableContextMenuView import TableContextMenuView
from app.views.EditTableDialogView import EditTableDialogView
from app.controllers.TableContextMenuController import TableContextMenuController
from app.controllers.EditTableDialogController import EditTableDialogController
from app.enums.TableContextMenuEnum import TableContextMenuEnum


class TablesController:
    def __init__(self, ParentWindow, TablesView, TablesModel, RelationshipsController, InheritancesController):
        self.__ParentWindow = ParentWindow
        self.__TablesView = TablesView
        self.__TablesModel = TablesModel
        self.__RelationshipsController = RelationshipsController
        self.__InheritancesController = InheritancesController
        self.__TableContextMenuView = TableContextMenuView(self.__ParentWindow)
        self.__TableContextMenuView.setupUI()
        self.__TableContextMenuController = TableContextMenuController(self.__TableContextMenuView)
        self.__TableInTransfer = None
        self.__isTableInTransfer = False
        self.__isContextMenuAtWork = False

    def addTable(self, cursorPosition):
        self.__TablesModel.addTable(cursorPosition)

    def deleteTable(self, cursorPosition):
        ObtainedTable = self.__TablesModel.getTableFromPosition(cursorPosition)
        if ObtainedTable is not None:
            dialogTitle = "WARNING"
            dialogText = "Are you sure about deleting this table?"
            ConfirmationDialog = ConfirmationDialogView(self.__ParentWindow, dialogTitle, dialogText)
            if ConfirmationDialog.displayDialog():
                self.__TablesModel.deleteSelectedTable(ObtainedTable)
                self.__RelationshipsController.deleteRelationshipByTable(ObtainedTable)
                self.__InheritancesController.deleteInheritanceByTable(ObtainedTable)

    def collapseTable(self, cursorPosition):
        ObtainedTable = self.__TablesModel.getTableFromPosition(cursorPosition)
        if ObtainedTable is not None:
            ObtainedTable.changeTableCollapseStatus()

    def editTable(self, cursorPosition):
        ObtainedTable = self.__TablesModel.getTableFromPosition(cursorPosition)
        if ObtainedTable is not None:
            EditTableDialog = EditTableDialogView(self.__ParentWindow, ObtainedTable)
            EditTableDialog.setupUi()
            EditTableDialogControl = EditTableDialogController(EditTableDialog, self, ObtainedTable)
            EditTableDialog.displayDialog()

    def selectTableInTransfer(self, cursorPosition):
        self.__TableInTransfer = self.__TablesModel.getTableFromPosition(cursorPosition)
        if self.__TableInTransfer is not None:
            self.__isTableInTransfer = True
            self.__TablesModel.deleteSelectedTable(self.__TableInTransfer)
            self.__TablesModel.addSelectedTable(self.__TableInTransfer)

    def unselectTableInTransfer(self, cursorPosition):
        self.__TableInTransfer.changeTablePosition(cursorPosition.x(), cursorPosition.y())
        self.__isTableInTransfer = False
        self.__TableInTransfer = None

    def updateTableInTransferPosition(self, cursorPosition):
        self.__TableInTransfer.changeTablePosition(cursorPosition.x(), cursorPosition.y())

    def selectDrawTempTable(self, cursorPosition):
        self.__TablesView.drawTempTable(cursorPosition)

    def selectDrawTables(self):
        self.__TablesView.drawTables()

    def getTableInTransferStatus(self):
        return self.__isTableInTransfer

    def getExtremeTableDimensions(self):
        extremeRightDimension = 0
        extremeBottomDimension = 0
        tables = self.__TablesModel.getTables()
        for ObtainedTable in tables:
            extremeRightDimension = max(extremeRightDimension, ObtainedTable.getRight())
            extremeBottomDimension = max(extremeBottomDimension, ObtainedTable.getBottom())
        return {
            "extremeRightDimension": extremeRightDimension,
            "extremeBottomDimension": extremeBottomDimension
        }

    def displayTableContextMenu(self, cursorPosition, globalCursorPosition):
        ObtainedTable = self.__TablesModel.getTableFromPosition(cursorPosition)
        if ObtainedTable is not None:
            self.__isContextMenuAtWork = True
            self.__TableContextMenuView.exec(globalCursorPosition)
            if self.__TableContextMenuController.getSelectCollapseTableStatus():
                self.__TableContextMenuController.unselectCollapseTable()
                self.__isContextMenuAtWork = False
                return TableContextMenuEnum.COLLAPSE
            elif self.__TableContextMenuController.getSelectEditTableStatus():
                self.__TableContextMenuController.unselectEditTable()
                self.__isContextMenuAtWork = False
                return TableContextMenuEnum.EDIT
            elif self.__TableContextMenuController.getSelectDeleteTableStatus():
                self.__TableContextMenuController.unselectDeleteTable()
                self.__isContextMenuAtWork = False
                return TableContextMenuEnum.DELETE
            return TableContextMenuEnum.NONE

    def unselectContextMenuAtWork(self):
        self.__isContextMenuAtWork = False

    def getContextMenuAtWorkStatus(self):
        return self.__isContextMenuAtWork

    def checkTableNameUnique(self, tableName):
        return self.__TablesModel.checkTableNameUnique(tableName)
