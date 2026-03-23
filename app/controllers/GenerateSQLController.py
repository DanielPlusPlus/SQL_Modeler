from app.views.GenerateSQLDialogView import GenerateSQLDialogView
from app.controllers.GenerateOracleSQLController import GenerateOracleSQLController
from app.controllers.GenerateMySQLController import GenerateMySQLController
from app.controllers.GenerateMSSQLController import GenerateMSSQLController
from app.controllers.GeneratePostgreSQLController import GeneratePostgreSQLController
from app.controllers.GenerateSQLDialogController import GenerateSQLDialogController


class GenerateSQLController:
    def __init__(self, ParentWindow, MainWindowController, TablesModel, RelationshipsModel, InheritancesModel):
        self.__ParentWindow = ParentWindow
        self.__MainWindowController = MainWindowController
        self.__TablesModel = TablesModel
        self.__RelationshipsModel = RelationshipsModel
        self.__InheritancesModel = InheritancesModel

    def displayDialog(self):
        oracleSQLCode = GenerateOracleSQLController(self.__TablesModel, self.__RelationshipsModel,
                                                    self.__InheritancesModel).generateSQLCode()
        mySQLCode = GenerateMySQLController(self.__TablesModel, self.__RelationshipsModel,
                                            self.__InheritancesModel).generateSQLCode()
        msSQLCode = GenerateMSSQLController(self.__TablesModel, self.__RelationshipsModel,
                                            self.__InheritancesModel).generateSQLCode()
        postgreSQLCode = GeneratePostgreSQLController(self.__TablesModel, self.__RelationshipsModel,
                                                      self.__InheritancesModel).generateSQLCode()

        GenerateSQLDialog = GenerateSQLDialogView(self.__ParentWindow)
        GenerateSQLDialog.setupUI(oracleSQLCode, mySQLCode, msSQLCode, postgreSQLCode)
        GenerateSQLControl = GenerateSQLDialogController(self.__ParentWindow, self.__MainWindowController,
                                                         GenerateSQLDialog)
        GenerateSQLDialog.displayDialog()
