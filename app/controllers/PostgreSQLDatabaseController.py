import psycopg2
from psycopg2 import OperationalError
from typing import override

from app.controllers.interfaces.DatabaseControllerInterface import DatabaseControllerInterface


class PostgreSQLDatabaseController(DatabaseControllerInterface):
    def __init__(self, params):
        self.__username = params["username"]
        self.__password = params["password"]
        self.__host = params["host"]
        self.__port = params["port"]
        self.__database = params["database"]

    @override
    def executeSQLCode(self, sqlCode):
        connection = None
        messages = []

        try:
            connection = psycopg2.connect(
                host=self.__host,
                port=self.__port,
                database=self.__database,
                user=self.__username,
                password=self.__password
            )
            messages.append("Connected to PostgreSQL database.")

            cursor = connection.cursor()

            statements = [stmt.strip() for stmt in sqlCode.split(';') if stmt.strip()]
            for statement in statements:
                try:
                    cursor.execute(statement)
                    messages.append(f"Executed:\n{statement}")
                except psycopg2.DatabaseError as e:
                    errorMessage = str(e)
                    messages.append(f"ERROR in statement:\n{statement}\n{errorMessage}")

            connection.commit()
            messages.append("All changes committed.")

        except OperationalError as e:
            messages.append(f"Connection or general error:\n{str(e)}")

        except Exception as e:
            messages.append(f"An unexpected error occurred:\n{str(e)}")

        finally:
            if connection is not None:
                connection.close()
                messages.append("Connection closed.")

        return "\n\n".join(messages)
