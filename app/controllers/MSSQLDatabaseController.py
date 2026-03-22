import pyodbc
from typing import override

from app.controllers.interfaces.DatabaseControllerInterface import DatabaseControllerInterface


class MSSQLDatabaseController(DatabaseControllerInterface):
    def __init__(self, params, driver="{ODBC Driver 17 for SQL Server}"):
        self.__connection_string = \
            (f"DRIVER={driver};SERVER={params["server"]},{params["port"]};"
             f"DATABASE={params["database"]};UID={params["username"]};PWD={params["password"]}")

    @override
    def executeSQLCode(self, sqlCode):
        connection = None
        messages = []

        try:
            connection = pyodbc.connect(self.__connection_string)
            messages.append("Connected to SQL Server database.")

            cursor = connection.cursor()

            statements = [stmt.strip() for stmt in sqlCode.split(';') if stmt.strip()]
            for statement in statements:
                try:
                    cursor.execute(statement)
                    messages.append(f"Executed:\n{statement}")
                except pyodbc.Error as e:
                    errorMessage = str(e)
                    messages.append(f"ERROR in statement:\n{statement}\n{errorMessage}")

            connection.commit()
            messages.append("All changes committed.")

        except pyodbc.Error as e:
            messages.append(f"Connection or general error:\n{str(e)}")

        except Exception as e:
            messages.append(f"An unexpected error occurred:\n{str(e)}")

        finally:
            if connection is not None:
                connection.close()
                messages.append("Connection closed.")

        return "\n\n".join(messages)