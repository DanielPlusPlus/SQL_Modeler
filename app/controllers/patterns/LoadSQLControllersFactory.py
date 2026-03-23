from app.controllers.LoadOracleSQLController import LoadOracleSQLController
from app.controllers.LoadMySQLController import LoadMySQLController
from app.controllers.LoadMSSQLController import LoadMSSQLController
from app.controllers.LoadPostgreSQLController import LoadPostgreSQLController
from app.enums.DatabasesEnum import DatabasesEnum


class LoadSQLControllersFactory:
    __controllers = {
        DatabasesEnum.ORACLE: LoadOracleSQLController,
        DatabasesEnum.MYSQL: LoadMySQLController,
        DatabasesEnum.MSSQL: LoadMSSQLController,
        DatabasesEnum.POSTGRESQL: LoadPostgreSQLController,
    }

    @staticmethod
    def createController(TablesModel, RelationshipsModel, InheritancesModel, DatabaseType):
        CreatedControllerClass = LoadSQLControllersFactory.__controllers[DatabaseType]
        return CreatedControllerClass(TablesModel, RelationshipsModel, InheritancesModel, DatabaseType)
