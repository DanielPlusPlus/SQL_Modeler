class ToolBarController:
    def __init__(self, ToolBarView, MenuBarController):
        self.__ToolBarView = ToolBarView
        self.__MenuBarController = MenuBarController
        self.__ToolBarView.actionExportDiagram.triggered.connect(self.__selectExportDiagramTool)
        self.__ToolBarView.actionGenerateSQL.triggered.connect(self.__selectGenerateSQLTool)
        self.__ToolBarView.actionCreateTable.triggered.connect(self.__selectCreateTableTool)
        self.__ToolBarView.actionCreate_1_1_Rel.triggered.connect(self.__selectCreate_1_1_RelTool)
        self.__ToolBarView.actionCreate_1_n_Rel.triggered.connect(self.__selectCreate_1_n_RelTool)
        self.__ToolBarView.actionCreate_n_n_Rel.triggered.connect(self.__selectCreate_n_n_RelTool)
        self.__ToolBarView.actionCreateInheritance.triggered.connect(self.__selectCreateInheritanceTool)

    def __selectCreateTableTool(self):
        self.__MenuBarController.selectCreateTableTool()

    def __selectCreate_1_1_RelTool(self):
        self.__MenuBarController.selectCreate_1_1_RelTool()

    def __selectCreate_1_n_RelTool(self):
        self.__MenuBarController.selectCreate_1_n_RelTool()

    def __selectCreate_n_n_RelTool(self):
        self.__MenuBarController.selectCreate_n_n_RelTool()

    def __selectCreateInheritanceTool(self):
        self.__MenuBarController.selectCreateInheritanceTool()

    def __selectExportDiagramTool(self):
        self.__MenuBarController.selectExportDiagramTool()

    def __selectGenerateSQLTool(self):
        self.__MenuBarController.selectGenerateSQLTool()
