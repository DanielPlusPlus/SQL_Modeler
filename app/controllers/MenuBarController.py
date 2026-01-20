from app.enums.ConnectionsStatusEnum import ConnectionsStatusEnum


class MenuBarController:
    def __init__(self, MenuBarView, MainWindowController, DrawingAreaController, LoadSQLController,
                 ExportDiagramController, GenerateSQLController):
        self.__MainWindowController = MainWindowController
        self.__DrawingAreaController = DrawingAreaController
        self.__LoadSQLController = LoadSQLController
        self.__ExportDiagramController = ExportDiagramController
        self.__GenerateSQLController = GenerateSQLController
        self.__isTableSelected = False
        self.__is_1_1_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION
        self.__is_1_n_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION
        self.__is_n_n_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION
        self.__isInheritanceSelected = ConnectionsStatusEnum.NOT_IN_MOTION
        MenuBarView.actionImportSQL.triggered.connect(self.__selectImportSQL)
        MenuBarView.actionExportDiagram.triggered.connect(self.selectExportDiagramTool)
        MenuBarView.actionGenerateSQL.triggered.connect(self.selectGenerateSQLTool)
        MenuBarView.actionQuit.triggered.connect(self.__selectQuit)
        MenuBarView.actionCreateTable.triggered.connect(self.selectCreateTableTool)
        MenuBarView.actionCreate_1_1_Rel.triggered.connect(self.selectCreate_1_1_RelTool)
        MenuBarView.actionCreate_1_n_Rel.triggered.connect(self.selectCreate_1_n_RelTool)
        MenuBarView.actionCreate_n_n_Rel.triggered.connect(self.selectCreate_n_n_RelTool)
        MenuBarView.actionCreateInheritance.triggered.connect(self.selectCreateInheritanceTool)

    def __selectImportSQL(self):
        self.__LoadSQLController.openFileDialogAndProcessSQL()

    def selectExportDiagramTool(self):
        self.__unselectAllTools()
        self.__DrawingAreaController.unselectConnectionsBeingDrawn()
        self.__DrawingAreaController.updateView()
        self.__ExportDiagramController.exportDiagramToPNG()

    def selectGenerateSQLTool(self):
        self.__unselectAllTools()
        self.__DrawingAreaController.unselectConnectionsBeingDrawn()
        self.__DrawingAreaController.updateView()
        self.__GenerateSQLController.displayDialog()

    def __selectQuit(self):
        self.__MainWindowController.closeWindow()

    def selectCreateTableTool(self):
        self.__unselectAllTools()
        self.__DrawingAreaController.unselectConnectionsBeingDrawn()
        self.__DrawingAreaController.updateView()
        self.__isTableSelected = True

    def unselectCreateTableTool(self):
        self.__isTableSelected = False

    def getCreateTableToolStatus(self):
        return self.__isTableSelected

    def selectCreate_1_1_RelTool(self):
        self.__unselectAllTools()
        self.__DrawingAreaController.unselectConnectionsBeingDrawn()
        self.__DrawingAreaController.updateView()
        self.__is_1_1_RelSelected = ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK

    def changeStatusToAfterClick_1_1_RelTool(self):
        self.__is_1_1_RelSelected = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK

    def unselectCreate_1_1_RelTool(self):
        self.__is_1_1_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION

    def getCreate_1_1_RelToolStatus(self):
        return self.__is_1_1_RelSelected

    def selectCreate_1_n_RelTool(self):
        self.__unselectAllTools()
        self.__DrawingAreaController.unselectConnectionsBeingDrawn()
        self.__DrawingAreaController.updateView()
        self.__is_1_n_RelSelected = ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK

    def changeStatusToAfterClick_1_n_RelTool(self):
        self.__is_1_n_RelSelected = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK

    def unselectCreate_1_n_RelTool(self):
        self.__is_1_n_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION

    def getCreate_1_n_RelToolStatus(self):
        return self.__is_1_n_RelSelected

    def selectCreate_n_n_RelTool(self):
        self.__unselectAllTools()
        self.__DrawingAreaController.unselectConnectionsBeingDrawn()
        self.__DrawingAreaController.updateView()
        self.__is_n_n_RelSelected = ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK

    def changeStatusToAfterClick_n_n_RelTool(self):
        self.__is_n_n_RelSelected = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK

    def unselectCreate_n_n_RelTool(self):
        self.__is_n_n_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION

    def getCreate_n_n_RelToolStatus(self):
        return self.__is_n_n_RelSelected

    def selectCreateInheritanceTool(self):
        self.__unselectAllTools()
        self.__DrawingAreaController.unselectConnectionsBeingDrawn()
        self.__DrawingAreaController.updateView()
        self.__isInheritanceSelected = ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK

    def changeStatusToAfterClickInheritanceTool(self):
        self.__isInheritanceSelected = ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK

    def unselectCreateInheritanceTool(self):
        self.__isInheritanceSelected = ConnectionsStatusEnum.NOT_IN_MOTION

    def getCreateInheritanceToolStatus(self):
        return self.__isInheritanceSelected

    def __unselectAllTools(self):
        self.__isTableSelected = False
        self.__is_1_1_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION
        self.__is_1_n_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION
        self.__is_n_n_RelSelected = ConnectionsStatusEnum.NOT_IN_MOTION
        self.__isInheritanceSelected = ConnectionsStatusEnum.NOT_IN_MOTION

