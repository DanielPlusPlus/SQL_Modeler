from app.views.ConfirmationDialogView import ConfirmationDialogView
from app.views.InheritanceContextMenuView import InheritanceContextMenuView
from app.controllers.ConnectionsController import ConnectionsController
from app.controllers.InheritanceContextMenuController import InheritanceContextMenuController
from app.enums.InheritanceContextMenuEnum import InheritanceContextMenuEnum


class InheritancesController(ConnectionsController):
    def __init__(self, ParentWindow, InheritanceView, InheritanceModel, TablesModel):
        super().__init__(ParentWindow, TablesModel)
        self.__InheritancesView = InheritanceView
        self.__InheritancesModel = InheritanceModel
        self.__isInheritanceBeingDrawn = False
        self.__isContextMenuAtWork = False

    def selectInheritanceBeingDrawn(self):
        self.__isInheritanceBeingDrawn = True

    def unselectInheritanceBeingDrawn(self):
        self.__isInheritanceBeingDrawn = False

    def getInheritanceBeingDrawnStatus(self):
        return self.__isInheritanceBeingDrawn

    def addInheritance(self):
        self.__InheritancesModel.addInheritance(self._FirstClickedTable, self._SecondClickedTable)
        self.resetTables()

    def deleteInheritance(self, cursorPosition):
        ObtainedInheritance = self.__InheritancesModel.getInheritanceFromPosition(cursorPosition)
        if ObtainedInheritance is not None:
            dialogTitle = "WARNING"
            dialogText = "Are you sure about deleting this inheritance?"
            ConfirmationDialog = ConfirmationDialogView(self._ParentWindow, dialogTitle, dialogText)
            if ConfirmationDialog.displayDialog():
                self.__InheritancesModel.deleteSelectedInheritance(ObtainedInheritance)

    def deleteInheritanceByTable(self, ObtainedTable):
        self.__InheritancesModel.deleteInheritanceByTable(ObtainedTable)

    def selectDrawInheritanceBeingDrawn(self, cursorPosition):
        self.__InheritancesView.drawInheritanceBeingDrawn(self._FirstClickedTable, cursorPosition)

    def selectDrawInheritances(self):
        self.__InheritancesView.drawInheritances()

    def displayInheritanceContextMenu(self, cursorPosition, globalCursorPosition):
        ObtainedInheritance = self.__InheritancesModel.getInheritanceFromPosition(cursorPosition)
        if ObtainedInheritance is not None:
            self.__isContextMenuAtWork = True
            InheritanceContextMenu = InheritanceContextMenuView(self._ParentWindow)
            InheritanceContextMenu.setupUI()
            InheritanceContextMenuControl = InheritanceContextMenuController(InheritanceContextMenu)
            InheritanceContextMenu.display(globalCursorPosition)
            if InheritanceContextMenuControl.getSelectDeleteInheritanceStatus():
                InheritanceContextMenuControl.unselectDeleteInheritance()
                self.__isContextMenuAtWork = False
                return InheritanceContextMenuEnum.DELETE
            return InheritanceContextMenuEnum.NONE

    def unselectContextMenuAtWork(self):
        self.__isContextMenuAtWork = False

    def getContextMenuAtWorkStatus(self):
        return self.__isContextMenuAtWork

