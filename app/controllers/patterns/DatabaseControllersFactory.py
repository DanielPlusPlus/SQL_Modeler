from app.controllers.OracleDatabaseController import OracleDatabaseController
from app.controllers.MySQLDatabaseController import MySQLDatabaseController
from app.controllers.MSSQLDatabaseController import MSSQLDatabaseController
from app.controllers.PostgreSQLDatabaseController import PostgreSQLDatabaseController
from app.enums.DatabasesEnum import DatabasesEnum


class DatabaseControllersFactory:
    __controllers = {
        DatabasesEnum.ORACLE: OracleDatabaseController,
        DatabasesEnum.MYSQL: MySQLDatabaseController,
        DatabasesEnum.MSSQL: MSSQLDatabaseController,
        DatabasesEnum.POSTGRESQL: PostgreSQLDatabaseController,
    }

    @staticmethod
    def createController(connectionParams, DatabaseType):
        CreatedControllerClass = DatabaseControllersFactory.__controllers[DatabaseType]
        return CreatedControllerClass(connectionParams)
