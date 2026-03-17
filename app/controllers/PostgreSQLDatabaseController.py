import psycopg2
from psycopg2 import OperationalError
from typing import override

from app.controllers.interfaces.DatabaseControllerInterface import DatabaseControllerInterface


class PostgreSQLDatabaseController(DatabaseControllerInterface):
    def __init__(self, username, password, host, port, database):
        self.__username = username
        self.__password = password
        self.__host = host
        self.__port = port
        self.__database = database

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
                    error_message = str(e)
                    messages.append(f"ERROR in statement:\n{statement}\n{error_message}")

            connection.commit()
            messages.append("All changes committed.")

        except OperationalError as e:
            messages.append(f"Connection or general error:\n{str(e)}")

        finally:
            if connection is not None:
                connection.close()
                messages.append("Connection closed.")

        return "\n\n".join(messages)
