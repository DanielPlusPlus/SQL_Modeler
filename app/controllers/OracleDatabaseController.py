import oracledb
from typing import override

from app.controllers.interfaces.DatabaseControllerInterface import DatabaseControllerInterface


class OracleDatabaseController(DatabaseControllerInterface):
    def __init__(self, params):
        self.__connectStr = \
            f"{params["username"]}/{params["password"]}@{params["host"]}:{params["port"]}/{params["serviceName"]}"

    @override
    def executeSQLCode(self, sqlCode):
        connection = None
        messages = []

        try:
            connection = oracledb.connect(self.__connectStr)
            messages.append("Connected to Oracle database.")

            with connection.cursor() as cursor:
                statements = [stmt.strip() for stmt in sqlCode.split(';') if stmt.strip()]
                for statement in statements:
                    try:
                        cursor.execute(statement)
                        messages.append(f"Executed:\n{statement}")
                    except oracledb.DatabaseError as e:
                        errorMessage = f"{type(e).__name__}: {e}"
                        messages.append(f"ERROR in statement:\n{statement}\n{errorMessage}")
                connection.commit()
                messages.append("All changes committed.")

        except oracledb.Error as e:
            messages.append(f"Connection or general error:\n{str(e)}")

        except Exception as e:
            messages.append(f"An unexpected error occurred:\n{str(e)}")

        finally:
            if connection is not None:
                connection.close()
                messages.append("Connection closed.")

        return "\n\n".join(messages)
