from app.views.OracleConnectionParamsDialogView import OracleConnectionParamsDialogView
from app.views.MySQLConnectionParamsDialogView import MySQLConnectionParamsDialogView
from app.views.MSSQLConnectionParamsDialogView import MSSQLConnectionParamsDialogView
from app.views.PostgreSQLConnectionParamsDialogView import PostgreSQLConnectionParamsDialogView
from app.enums.DatabasesEnum import DatabasesEnum


class ConnectionParamsDialogViewsFactory:
    __views = {
        DatabasesEnum.ORACLE: OracleConnectionParamsDialogView,
        DatabasesEnum.MYSQL: MySQLConnectionParamsDialogView,
        DatabasesEnum.MSSQL: MSSQLConnectionParamsDialogView,
        DatabasesEnum.POSTGRESQL: PostgreSQLConnectionParamsDialogView,
    }

    @staticmethod
    def createController(ParentWindow, DatabaseType):
        CreatedViewClass = ConnectionParamsDialogViewsFactory.__views[DatabaseType]
        return CreatedViewClass(ParentWindow)
