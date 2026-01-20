import unittest
from unittest.mock import MagicMock, patch
import sys

from app.controllers.DrawingAreaController import DrawingAreaController
from app.enums.ConnectionsStatusEnum import ConnectionsStatusEnum


class TestDrawingAreaController(unittest.TestCase):

    def setUp(self):
        modulesToDelete = list(sys.modules.keys())
        for moduleName in modulesToDelete:
            if moduleName.startswith('app.controllers.DrawingAreaController') or \
                    moduleName.startswith('app.enums') or \
                    moduleName.startswith('PySide6.QtCore'):
                if moduleName in sys.modules:
                    del sys.modules[moduleName]

        self.patcherQPoint = patch('app.controllers.DrawingAreaController.QPoint', new_callable=MagicMock)
        self.mockQPointClass = self.patcherQPoint.start()

        self.patcherQtMouseButton = patch('app.controllers.DrawingAreaController.Qt.MouseButton',
                                          new_callable=MagicMock)
        self.mockQtMouseButton = self.patcherQtMouseButton.start()

        self.controller = DrawingAreaController()

        self.mockDrawingAreaView = MagicMock()
        self.mockMainWindowController = MagicMock()
        self.mockMenuBarController = MagicMock()
        self.mockTablesController = MagicMock()
        self.mockRelationshipsController = MagicMock()
        self.mockInheritancesController = MagicMock()

        self.controller.setDrawingAreaView(self.mockDrawingAreaView)
        self.controller.setMainWindowController(self.mockMainWindowController)
        self.controller.setMenuBarController(self.mockMenuBarController)
        self.controller.setTablesController(self.mockTablesController)
        self.controller.setRelationshipsController(self.mockRelationshipsController)
        self.controller.setInheritancesController(self.mockInheritancesController)

        self.mockQPointInstanceInController = self.controller._DrawingAreaController__cursorPosition

    def tearDown(self):
        self.patcherQPoint.stop()
        self.patcherQtMouseButton.stop()

    def testSetDrawingAreaView(self):
        mockView = MagicMock()
        self.controller.setDrawingAreaView(mockView)
        self.assertIs(self.controller._DrawingAreaController__DrawingAreaView, mockView)

    def testSetMainWindowController(self):
        mockController = MagicMock()
        self.controller.setMainWindowController(mockController)
        self.assertIs(self.controller._DrawingAreaController__MainWindowController, mockController)

    def testSetMenuBarController(self):
        mockController = MagicMock()
        self.controller.setMenuBarController(mockController)
        self.assertIs(self.controller._DrawingAreaController__MenuBarController, mockController)

    def testSetTablesController(self):
        mockController = MagicMock()
        self.controller.setTablesController(mockController)
        self.assertIs(self.controller._DrawingAreaController__TablesController, mockController)

    def testSetRelationshipsController(self):
        mockController = MagicMock()
        self.controller.setRelationshipsController(mockController)
        self.assertIs(self.controller._DrawingAreaController__RelationshipsController, mockController)

    def testSetInheritancesController(self):
        mockController = MagicMock()
        self.controller.setInheritancesController(mockController)
        self.assertIs(self.controller._DrawingAreaController__InheritancesController, mockController)

    def testHandleMouseMove(self):
        mockEvent = MagicMock()
        mockPosition = MagicMock()

        mockPointFromEvent = MagicMock()

        mockEvent.position.return_value = mockPosition
        mockPosition.toPoint.return_value = mockPointFromEvent

        self.controller.handleMouseMove(mockEvent)

        self.assertIs(self.controller._DrawingAreaController__cursorPosition, mockPointFromEvent)
        self.mockMainWindowController.updateStatusBarInView.assert_called_once_with(mockPointFromEvent)

    def testHandleMousePressLeftButtonCreateTableToolActive(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = True

        expectedCursorPos = self.mockQPointInstanceInController
        self.controller._DrawingAreaController__cursorPosition = expectedCursorPos

        self.controller.handleMousePress(mockEvent)

        self.mockTablesController.addTable.assert_called_once_with(expectedCursorPos)
        self.mockMenuBarController.unselectCreateTableTool.assert_called_once()

        self.mockMenuBarController.getCreate_1_1_RelToolStatus.assert_not_called()
        self.mockTablesController.unselectTableInTransfer.assert_not_called()

    def testHandleMousePressLeftButton11RelBeforeClickSuccess(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK
        self.mockRelationshipsController.setFirstClickedTable.return_value = True
        self.mockRelationshipsController.setFirstSelectedColumnName.return_value = True

        expectedCursorPos = self.mockQPointInstanceInController
        self.controller._DrawingAreaController__cursorPosition = expectedCursorPos

        self.controller.handleMousePress(mockEvent)

        self.mockRelationshipsController.setFirstClickedTable.assert_called_once_with(expectedCursorPos)
        self.mockRelationshipsController.setFirstSelectedColumnName.assert_called_once()
        self.mockMenuBarController.changeStatusToAfterClick_1_1_RelTool.assert_called_once()
        self.mockRelationshipsController.selectRelationshipBeingDrawn.assert_called_once()

    def testHandleMousePressLeftButton11RelAfterClickSuccess(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK
        self.mockRelationshipsController.setSecondClickedTable.return_value = True
        self.mockRelationshipsController.setSecondSelectedColumnName.return_value = True

        expectedCursorPos = self.mockQPointInstanceInController
        self.controller._DrawingAreaController__cursorPosition = expectedCursorPos

        self.controller.handleMousePress(mockEvent)

        self.mockRelationshipsController.setSecondClickedTable.assert_called_once_with(expectedCursorPos)
        self.mockRelationshipsController.setSecondSelectedColumnName.assert_called_once()
        self.mockRelationshipsController.add_1_1_Relationship.assert_called_once()
        self.mockMenuBarController.unselectCreate_1_1_RelTool.assert_called_once()
        self.mockRelationshipsController.unselectRelationshipBeingDrawn.assert_called_once()

    def testHandleMousePressLeftButton1NRelBeforeClickSuccess(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK
        self.mockRelationshipsController.setFirstClickedTable.return_value = True
        self.mockRelationshipsController.setFirstSelectedColumnName.return_value = True

        expectedCursorPos = self.mockQPointInstanceInController
        self.controller._DrawingAreaController__cursorPosition = expectedCursorPos

        self.controller.handleMousePress(mockEvent)

        self.mockRelationshipsController.setFirstClickedTable.assert_called_once_with(expectedCursorPos)
        self.mockRelationshipsController.setFirstSelectedColumnName.assert_called_once()
        self.mockMenuBarController.changeStatusToAfterClick_1_n_RelTool.assert_called_once()
        self.mockRelationshipsController.selectRelationshipBeingDrawn.assert_called_once()

    def testHandleMousePressLeftButtonInheritanceAfterClickSuccess(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_n_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreateInheritanceToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK
        self.mockInheritancesController.setSecondClickedTable.return_value = True

        expectedCursorPos = self.mockQPointInstanceInController
        self.controller._DrawingAreaController__cursorPosition = expectedCursorPos

        self.controller.handleMousePress(mockEvent)

        self.mockInheritancesController.setSecondClickedTable.assert_called_once_with(expectedCursorPos)
        self.mockInheritancesController.addInheritance.assert_called_once()
        self.mockMenuBarController.unselectCreateInheritanceTool.assert_called_once()
        self.mockInheritancesController.unselectInheritanceBeingDrawn.assert_called_once()

    def testHandleMousePressLeftButtonTableInTransferStatus(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_n_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreateInheritanceToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION

        self.mockTablesController.getTableInTransferStatus.return_value = True

        expectedCursorPos = self.mockQPointInstanceInController
        self.controller._DrawingAreaController__cursorPosition = expectedCursorPos

        self.controller.handleMousePress(mockEvent)

        self.mockTablesController.unselectTableInTransfer.assert_called_once_with(expectedCursorPos)

        self.mockTablesController.addTable.assert_not_called()
        self.mockTablesController.selectTableInTransfer.assert_not_called()

    def testHandleMousePressLeftButtonTablesContextMenuAtWork(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_n_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreateInheritanceToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockTablesController.getTableInTransferStatus.return_value = False

        self.mockTablesController.getContextMenuAtWorkStatus.return_value = True

        self.controller._DrawingAreaController__cursorPosition = self.mockQPointInstanceInController

        self.controller.handleMousePress(mockEvent)

        self.mockTablesController.unselectContextMenuAtWork.assert_called_once()
        self.mockRelationshipsController.unselectContextMenuAtWork.assert_not_called()

    def testHandleMousePressLeftButtonRelationshipsContextMenuAtWork(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_n_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreateInheritanceToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockTablesController.getTableInTransferStatus.return_value = False
        self.mockTablesController.getContextMenuAtWorkStatus.return_value = False

        self.mockRelationshipsController.getContextMenuAtWorkStatus.return_value = True

        self.controller._DrawingAreaController__cursorPosition = self.mockQPointInstanceInController

        self.controller.handleMousePress(mockEvent)

        self.mockRelationshipsController.unselectContextMenuAtWork.assert_called_once()
        self.mockTablesController.unselectContextMenuAtWork.assert_not_called()

    def testHandleMousePressLeftButtonDefaultSelectTableInTransfer(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.LeftButton

        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_n_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreateInheritanceToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockTablesController.getTableInTransferStatus.return_value = False
        self.mockTablesController.getContextMenuAtWorkStatus.return_value = False
        self.mockRelationshipsController.getContextMenuAtWorkStatus.return_value = False
        self.mockInheritancesController.getContextMenuAtWorkStatus.return_value = False

        expectedCursorPos = self.mockQPointInstanceInController
        self.controller._DrawingAreaController__cursorPosition = expectedCursorPos

        self.controller.handleMousePress(mockEvent)

        self.mockTablesController.selectTableInTransfer.assert_called_once_with(expectedCursorPos)

        self.mockTablesController.addTable.assert_not_called()

    def testHandleMousePressRightButtonCreateTableToolActive(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.RightButton
        self.mockMenuBarController.getCreateTableToolStatus.return_value = True

        self.controller.handleMousePress(mockEvent)
        self.mockMenuBarController.unselectCreateTableTool.assert_called_once()

    def testHandleMousePressRightButton11RelToolActive(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.RightButton
        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK

        self.controller.handleMousePress(mockEvent)
        self.mockRelationshipsController.unselectRelationshipBeingDrawn.assert_called_once()
        self.mockMenuBarController.unselectCreate_1_1_RelTool.assert_called_once()

    def testHandleMousePressRightButton1NRelToolActive(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.RightButton
        self._setAllToolsNotInMotion()
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK

        self.controller.handleMousePress(mockEvent)
        self.mockRelationshipsController.unselectRelationshipBeingDrawn.assert_called_once()
        self.mockMenuBarController.unselectCreate_1_n_RelTool.assert_called_once()

    def testHandleMousePressRightButtonNNRelToolActive(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.RightButton
        self._setAllToolsNotInMotion()
        self.mockMenuBarController.getCreate_n_n_RelToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK

        self.controller.handleMousePress(mockEvent)
        self.mockRelationshipsController.unselectRelationshipBeingDrawn.assert_called_once()
        self.mockMenuBarController.unselectCreate_n_n_RelTool.assert_called_once()

    def testHandleMousePressRightButtonInheritanceToolActive(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.RightButton
        self._setAllToolsNotInMotion()
        self.mockMenuBarController.getCreateInheritanceToolStatus.return_value = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK

        self.controller.handleMousePress(mockEvent)
        self.mockInheritancesController.unselectInheritanceBeingDrawn.assert_called_once()
        self.mockMenuBarController.unselectCreateInheritanceTool.assert_called_once()

    def testHandleMousePressRightButtonTableContextMenuAtWork(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.RightButton
        self._setAllToolsNotInMotion()
        self.mockTablesController.getTableInTransferStatus.return_value = False

        self.mockTablesController.getContextMenuAtWorkStatus.return_value = True

        self.controller.handleMousePress(mockEvent)
        self.mockTablesController.unselectContextMenuAtWork.assert_called_once()
        self.mockRelationshipsController.unselectContextMenuAtWork.assert_not_called()

    def testHandleMousePressRightButtonRelationshipContextMenuAtWork(self):
        mockEvent = MagicMock()
        mockEvent.button.return_value = self.mockQtMouseButton.RightButton
        self._setAllToolsNotInMotion()
        self.mockTablesController.getTableInTransferStatus.return_value = False
        self.mockTablesController.getContextMenuAtWorkStatus.return_value = False

        self.mockRelationshipsController.getContextMenuAtWorkStatus.return_value = True

        self.controller.handleMousePress(mockEvent)
        self.mockRelationshipsController.unselectContextMenuAtWork.assert_called_once()
        self.mockTablesController.unselectContextMenuAtWork.assert_not_called()

    def _setAllToolsNotInMotion(self):
        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockMenuBarController.getCreate_1_1_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_1_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreate_n_n_RelToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION
        self.mockMenuBarController.getCreateInheritanceToolStatus.return_value = ConnectionsStatusEnum.NOT_IN_MOTION

    def testHandlePaintEventCreateTableToolActive(self):
        self.mockMenuBarController.getCreateTableToolStatus.return_value = True
        self.controller._DrawingAreaController__cursorPosition = self.mockQPointInstanceInController

        self.controller.handlePaintEvent()

        self.mockTablesController.selectDrawTempTable.assert_called_once_with(
            self.controller._DrawingAreaController__cursorPosition
        )
        self.mockTablesController.selectDrawTables.assert_called_once()
        self.mockRelationshipsController.selectDrawRelationships.assert_called_once()
        self.mockInheritancesController.selectDrawInheritances.assert_called_once()
        self.mockTablesController.updateTableInTransferPosition.assert_not_called()

    def testHandlePaintEventTableInTransferStatus(self):
        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockTablesController.getTableInTransferStatus.return_value = True
        self.controller._DrawingAreaController__cursorPosition = self.mockQPointInstanceInController

        self.controller.handlePaintEvent()

        self.mockTablesController.updateTableInTransferPosition.assert_called_once_with(
            self.controller._DrawingAreaController__cursorPosition
        )
        self.mockTablesController.selectDrawTables.assert_called_once()
        self.mockRelationshipsController.selectDrawRelationships.assert_called_once()
        self.mockInheritancesController.selectDrawInheritances.assert_called_once()

    def testHandlePaintEventRelationshipBeingDrawnStatus(self):
        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockTablesController.getTableInTransferStatus.return_value = False
        self.mockRelationshipsController.getRelationshipBeingDrawnStatus.return_value = True
        self.controller._DrawingAreaController__cursorPosition = self.mockQPointInstanceInController

        self.controller.handlePaintEvent()

        self.mockRelationshipsController.selectDrawRelationshipBeingDrawn.assert_called_once_with(
            self.controller._DrawingAreaController__cursorPosition
        )
        self.mockTablesController.selectDrawTables.assert_called_once()
        self.mockRelationshipsController.selectDrawRelationships.assert_called_once()
        self.mockInheritancesController.selectDrawInheritances.assert_called_once()

    def testHandlePaintEventInheritanceBeingDrawnStatus(self):
        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockTablesController.getTableInTransferStatus.return_value = False
        self.mockRelationshipsController.getRelationshipBeingDrawnStatus.return_value = False
        self.mockInheritancesController.getInheritanceBeingDrawnStatus.return_value = True
        self.controller._DrawingAreaController__cursorPosition = self.mockQPointInstanceInController

        self.controller.handlePaintEvent()

        self.mockInheritancesController.selectDrawInheritanceBeingDrawn.assert_called_once_with(
            self.controller._DrawingAreaController__cursorPosition
        )
        self.mockTablesController.selectDrawTables.assert_called_once()
        self.mockRelationshipsController.selectDrawRelationships.assert_called_once()
        self.mockInheritancesController.selectDrawInheritances.assert_called_once()

    def testHandlePaintEventNoSpecialStatus(self):
        self.mockMenuBarController.getCreateTableToolStatus.return_value = False
        self.mockTablesController.getTableInTransferStatus.return_value = False
        self.mockRelationshipsController.getRelationshipBeingDrawnStatus.return_value = False
        self.mockInheritancesController.getInheritanceBeingDrawnStatus.return_value = False
        self.controller._DrawingAreaController__cursorPosition = self.mockQPointInstanceInController

        self.controller.handlePaintEvent()

        self.mockTablesController.selectDrawTempTable.assert_not_called()
        self.mockTablesController.updateTableInTransferPosition.assert_not_called()
        self.mockRelationshipsController.selectDrawRelationshipBeingDrawn.assert_not_called()
        self.mockInheritancesController.selectDrawInheritanceBeingDrawn.assert_not_called()

        self.mockTablesController.selectDrawTables.assert_called_once()
        self.mockRelationshipsController.selectDrawRelationships.assert_called_once()
        self.mockInheritancesController.selectDrawInheritances.assert_called_once()

    def testConvertCursorPositionToGlobal(self):
        mockCursorPos = MagicMock()
        mockGlobalPos = MagicMock()
        self.mockDrawingAreaView.mapToGlobal.return_value = mockGlobalPos

        result = self.controller._DrawingAreaController__convertCursorPositionToGlobal(mockCursorPos)

        self.mockDrawingAreaView.mapToGlobal.assert_called_once_with(mockCursorPos)
        self.assertIs(result, mockGlobalPos)

    def testUpdateView(self):
        self.controller.updateView()
        self.mockDrawingAreaView.update.assert_called_once()

    def testUnselectConnectionsBeingDrawn(self):
        self.controller.unselectConnectionsBeingDrawn()
        self.mockRelationshipsController.unselectRelationshipBeingDrawn.assert_called_once()
        self.mockInheritancesController.unselectInheritanceBeingDrawn.assert_called_once()


if __name__ == '__main__':
    unittest.main()