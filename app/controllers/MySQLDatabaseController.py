import mysql.connector
from typing import override

from app.controllers.interfaces.DatabaseControllerInterface import DatabaseControllerInterface


class MySQLDatabaseController(DatabaseControllerInterface):
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
            connection = mysql.connector.connect(
                host=self.__host,
                port=self.__port,
                database=self.__database,
                user=self.__username,
                password=self.__password
            )
            messages.append("Connected to MySQL database.")

            cursor = connection.cursor()

            statements = [stmt.strip() for stmt in sqlCode.split(';') if stmt.strip()]
            for statement in statements:
                try:
                    cursor.execute(statement)
                    messages.append(f"Executed:\n{statement}")
                except mysql.connector.Error as e:
                    error_message = str(e)
                    messages.append(f"ERROR in statement:\n{statement}\n{error_message}")

            connection.commit()
            messages.append("All changes committed.")

        except mysql.connector.Error as e:
            messages.append(f"Connection or general error:\n{str(e)}")

        finally:
            if connection is not None and connection.is_connected():
                connection.close()
                messages.append("Connection closed.")

        return "\n\n".join(messages)
