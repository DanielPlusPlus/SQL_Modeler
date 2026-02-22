from PySide6.QtCore import Qt, QPoint

from app.enums.ConnectionsStatusEnum import ConnectionsStatusEnum
from app.enums.TableContextMenuEnum import TableContextMenuEnum
from app.enums.RelationshipContextMenuEnum import RelationshipContextMenuEnum
from app.enums.InheritanceContextMenuEnum import InheritanceContextMenuEnum


class DrawingAreaController:
    def __init__(self):
        self.__DrawingAreaView = None
        self.__cursorPosition = QPoint()
        self.__MainWindowController = None
        self.__MenuBarController = None
        self.__TablesController = None
        self.__RelationshipsController = None
        self.__InheritancesController = None
        self.__scaleFactor = 1.0

    def setDrawingAreaView(self, DrawingAreaView):
        self.__DrawingAreaView = DrawingAreaView

    def setMainWindowController(self, MainWindowController):
        self.__MainWindowController = MainWindowController

    def setMenuBarController(self, MenuBarController):
        self.__MenuBarController = MenuBarController

    def setTablesController(self, TablesController):
        self.__TablesController = TablesController

    def setRelationshipsController(self, RelationshipsController):
        self.__RelationshipsController = RelationshipsController

    def setInheritancesController(self, InheritancesController):
        self.__InheritancesController = InheritancesController

    def handleMouseMove(self, event):
        self.__cursorPosition = event.position().toPoint()
        self.__MainWindowController.updateStatusBarInView(self.__cursorPosition)

    def handleMousePress(self, event):
        self.__unselectCloseMainWindowWithoutConfirmation()
        if event.button() == Qt.MouseButton.LeftButton:
            if self.__MenuBarController.getCreateTableToolStatus():
                self.__TablesController.addTable(self.__cursorPosition)
                self.__MenuBarController.unselectCreateTableTool()
                self.__updateMinimumSize()

            elif (self.__MenuBarController.getCreate_1_1_RelToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK):
                if self.__RelationshipsController.setFirstClickedTable(self.__cursorPosition):
                    if self.__RelationshipsController.setFirstSelectedColumnName():
                        self.__MenuBarController.changeStatusToAfterClick_1_1_RelTool()
                        self.__RelationshipsController.selectRelationshipBeingDrawn()
            elif (self.__MenuBarController.getCreate_1_1_RelToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK):
                if self.__RelationshipsController.setSecondClickedTable(self.__cursorPosition):
                    if self.__RelationshipsController.setSecondSelectedColumnName():
                        self.__RelationshipsController.add_1_1_Relationship()
                        self.__MenuBarController.unselectCreate_1_1_RelTool()
                        self.__RelationshipsController.unselectRelationshipBeingDrawn()

            elif (self.__MenuBarController.getCreate_1_n_RelToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK):
                if self.__RelationshipsController.setFirstClickedTable(self.__cursorPosition):
                    if self.__RelationshipsController.setFirstSelectedColumnName():
                        self.__MenuBarController.changeStatusToAfterClick_1_n_RelTool()
                        self.__RelationshipsController.selectRelationshipBeingDrawn()
            elif (self.__MenuBarController.getCreate_1_n_RelToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK):
                if self.__RelationshipsController.setSecondClickedTable(self.__cursorPosition):
                    if self.__RelationshipsController.setSecondSelectedColumnName():
                        self.__RelationshipsController.add_1_n_Relationship()
                        self.__MenuBarController.unselectCreate_1_n_RelTool()
                        self.__RelationshipsController.unselectRelationshipBeingDrawn()

            elif (self.__MenuBarController.getCreate_n_n_RelToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK):
                if self.__RelationshipsController.setFirstClickedTable(self.__cursorPosition):
                    if self.__RelationshipsController.setFirstSelectedColumnName():
                        self.__MenuBarController.changeStatusToAfterClick_n_n_RelTool()
                        self.__RelationshipsController.selectRelationshipBeingDrawn()
            elif (self.__MenuBarController.getCreate_n_n_RelToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK):
                if self.__RelationshipsController.setSecondClickedTable(self.__cursorPosition):
                    if self.__RelationshipsController.setSecondSelectedColumnName():
                        self.__RelationshipsController.add_n_n_Relationship()
                        self.__MenuBarController.unselectCreate_n_n_RelTool()
                        self.__RelationshipsController.unselectRelationshipBeingDrawn()

            elif (self.__MenuBarController.getCreateInheritanceToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK):
                if self.__InheritancesController.setFirstClickedTable(self.__cursorPosition):
                    self.__MenuBarController.changeStatusToAfterClickInheritanceTool()
                    self.__InheritancesController.selectInheritanceBeingDrawn()
            elif (self.__MenuBarController.getCreateInheritanceToolStatus()
                  is ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK):
                if self.__InheritancesController.setSecondClickedTable(self.__cursorPosition):
                    self.__InheritancesController.addInheritance()
                    self.__MenuBarController.unselectCreateInheritanceTool()
                    self.__InheritancesController.unselectInheritanceBeingDrawn()

            elif self.__TablesController.getTableInTransferStatus():
                self.__TablesController.unselectTableInTransfer(self.__cursorPosition)
                self.__updateMinimumSize()
            elif self.__TablesController.getContextMenuAtWorkStatus():
                self.__TablesController.unselectContextMenuAtWork()
            elif self.__RelationshipsController.getContextMenuAtWorkStatus():
                self.__RelationshipsController.unselectContextMenuAtWork()
            elif self.__InheritancesController.getContextMenuAtWorkStatus():
                self.__InheritancesController.unselectContextMenuAtWork()
            else:
                self.__TablesController.selectTableInTransfer(self.__cursorPosition)
        elif event.button() == Qt.MouseButton.RightButton:
            if self.__MenuBarController.getCreateTableToolStatus():
                self.__MenuBarController.unselectCreateTableTool()

            elif (self.__MenuBarController.getCreate_1_1_RelToolStatus()
                  is not ConnectionsStatusEnum.NOT_IN_MOTION):
                self.__RelationshipsController.unselectRelationshipBeingDrawn()
                self.__MenuBarController.unselectCreate_1_1_RelTool()
            elif (self.__MenuBarController.getCreate_1_n_RelToolStatus()
                  is not ConnectionsStatusEnum.NOT_IN_MOTION):
                self.__RelationshipsController.unselectRelationshipBeingDrawn()
                self.__MenuBarController.unselectCreate_1_n_RelTool()
            elif (self.__MenuBarController.getCreate_n_n_RelToolStatus()
                  is not ConnectionsStatusEnum.NOT_IN_MOTION):
                self.__RelationshipsController.unselectRelationshipBeingDrawn()
                self.__MenuBarController.unselectCreate_n_n_RelTool()
            elif (self.__MenuBarController.getCreateInheritanceToolStatus()
                  is not ConnectionsStatusEnum.NOT_IN_MOTION):
                self.__InheritancesController.unselectInheritanceBeingDrawn()
                self.__MenuBarController.unselectCreateInheritanceTool()

            elif self.__TablesController.getTableInTransferStatus():
                pass
            elif self.__TablesController.getContextMenuAtWorkStatus():
                self.__TablesController.unselectContextMenuAtWork()
            elif self.__RelationshipsController.getContextMenuAtWorkStatus():
                self.__RelationshipsController.unselectContextMenuAtWork()
            elif self.__InheritancesController.getContextMenuAtWorkStatus():
                self.__InheritancesController.unselectContextMenuAtWork()
            elif (not self.__TablesController.getContextMenuAtWorkStatus()
                  and not self.__RelationshipsController.getContextMenuAtWorkStatus()
                  and not self.__InheritancesController.getContextMenuAtWorkStatus()):
                globalCursorPosition = self.__convertCursorPositionToGlobal(self.__cursorPosition)
                result = self.__TablesController.displayTableContextMenu(self.__cursorPosition,
                                                                         globalCursorPosition)
                if result is TableContextMenuEnum.COLLAPSE_EXPAND:
                    self.__TablesController.collapseExpandTable(self.__cursorPosition)
                elif result is TableContextMenuEnum.EDIT:
                    self.__TablesController.editTable(self.__cursorPosition)
                elif result is TableContextMenuEnum.DELETE:
                    self.__TablesController.deleteTable(self.__cursorPosition)
                else:
                    result = self.__RelationshipsController.displayRelationshipContextMenu(self.__cursorPosition,
                                                                                           globalCursorPosition)

                    if result is RelationshipContextMenuEnum.DELETE:
                        self.__RelationshipsController.deleteRelationship(self.__cursorPosition)

                    result = self.__InheritancesController.displayInheritanceContextMenu(self.__cursorPosition,
                                                                                         globalCursorPosition)
                    if result is InheritanceContextMenuEnum.DELETE:
                        self.__InheritancesController.deleteInheritance(self.__cursorPosition)
        elif event.button() == Qt.MiddleButton:
            self.__scaleFactor = 1.0

    def handleWheelMove(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.__scaleFactor = min(2.0, round(self.__scaleFactor + 0.1, 1))
        else:
            self.__scaleFactor = max(0.1, round(self.__scaleFactor - 0.1, 1))

        print(self.__scaleFactor)

    def handlePaintEvent(self):
        self.__RelationshipsController.selectDrawRelationships()
        self.__InheritancesController.selectDrawInheritances()
        self.__TablesController.selectDrawTables()
        if self.__MenuBarController.getCreateTableToolStatus():
            self.__TablesController.selectDrawTempTable(self.__cursorPosition)
        elif self.__TablesController.getTableInTransferStatus():
            self.__TablesController.updateTableInTransferPosition(self.__cursorPosition)
        elif self.__RelationshipsController.getRelationshipBeingDrawnStatus():
            self.__RelationshipsController.selectDrawRelationshipBeingDrawn(self.__cursorPosition)
        elif self.__InheritancesController.getInheritanceBeingDrawnStatus():
            self.__InheritancesController.selectDrawInheritanceBeingDrawn(self.__cursorPosition)

    def __updateMinimumSize(self):
        extremeTableDimensions = self.__TablesController.getExtremeTableDimensions()
        minimumWidth = max(self.__DrawingAreaView.getMinimumWidth(),
                           extremeTableDimensions["extremeRightDimension"] + 50)
        minimumHeight = max(self.__DrawingAreaView.getMinimumHeight(),
                            extremeTableDimensions["extremeBottomDimension"] + 50)
        self.__DrawingAreaView.setMinimumSize(minimumWidth, minimumHeight)

    def updateView(self):
        self.__DrawingAreaView.update()

    def unselectConnectionsBeingDrawn(self):
        self.__RelationshipsController.unselectRelationshipBeingDrawn()
        self.__InheritancesController.unselectInheritanceBeingDrawn()

    def __convertCursorPositionToGlobal(self, cursorPosition):
        return self.__DrawingAreaView.mapToGlobal(cursorPosition)

    def __unselectCloseMainWindowWithoutConfirmation(self):
        self.__MainWindowController.unselectCloseWithoutConfirmation()
