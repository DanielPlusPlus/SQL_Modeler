from app.controllers.OracleConnectionParamsDialogController import OracleConnectionParamsDialogController
from app.controllers.MySQLConnectionParamsDialogController import MySQLConnectionParamsDialogController
from app.controllers.MSSQLConnectionParamsDialogController import MSSQLConnectionParamsDialogController
from app.controllers.PostgreSQLConnectionParamsDialogController import PostgreConnectionParamsDialogController
from app.enums.DatabasesEnum import DatabasesEnum


class ConnectionParamsDialogControllersFactory:
    __controllers = {
        DatabasesEnum.ORACLE: OracleConnectionParamsDialogController,
        DatabasesEnum.MYSQL: MySQLConnectionParamsDialogController,
        DatabasesEnum.MSSQL: MSSQLConnectionParamsDialogController,
        DatabasesEnum.POSTGRESQL: PostgreConnectionParamsDialogController,
    }

    @staticmethod
    def createController(ConnectionParamsDialogView, DatabaseType):
        CreatedControllerClass = ConnectionParamsDialogControllersFactory.__controllers[DatabaseType]
        return CreatedControllerClass(ConnectionParamsDialogView)
