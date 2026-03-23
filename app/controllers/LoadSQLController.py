from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.controllers.patterns.LoadSQLControllersFactory import LoadSQLControllersFactory


class LoadSQLController:
    def __init__(self, ParentWindow, TablesModel, RelationshipsModel, InheritancesModel):
        self.__ParentWindow = ParentWindow
        self.__TablesModel = TablesModel
        self.__RelationshipsModel = RelationshipsModel
        self.__InheritancesModel = InheritancesModel

    def openFileDialogAndProcessSQL(self, DatabaseType):
        captions = (u"Select Oracle SQL File", u"Select MySQL SQL File",
                    u"Select MSSQL SQL File", u"Select Postgre SQL File")
        filePath, _ = QFileDialog.getOpenFileName(
            self.__ParentWindow,
            captions[DatabaseType.value - 1],
            "",
            "SQL Files (*.sql);;All Files (*)"
        )

        if filePath:
            try:
                with open(filePath, "r", encoding="utf-8") as file:
                    sqlCode = file.read()

                LoadSQLControllersFactory.createController(self.__TablesModel, self.__RelationshipsModel,
                                                           self.__InheritancesModel, DatabaseType).parseSQLCode(sqlCode)

                QMessageBox.information(
                    self.__ParentWindow,
                    "Success",
                    "SQL file successfully processed!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self.__ParentWindow,
                    "Error",
                    f"An error occurred while processing the file: {str(e)}"
                )
