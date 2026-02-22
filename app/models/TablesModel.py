from PySide6.QtCore import QPoint

from app.models.TableModel import TableModel


class TablesModel:
    def __init__(self):
        self.tables = []
        self.tableNumber = 1

    def addTable(self, position, width=100, rowsHeight=20, minRowsNumber=5):
        CreatedTable = TableModel(position.x(), position.y(), width, rowsHeight, minRowsNumber, self.tableNumber)
        self.tables.append(CreatedTable)
        self.tableNumber += 1

    def addSelectedTable(self, SelectedTable):
        self.tables.append(SelectedTable)

    def clearTables(self):
        self.tables.clear()

    def getTables(self):
        return self.tables

    def deleteSelectedTable(self, SelectedTable):
        self.tables.remove(SelectedTable)

    def getTableFromPosition(self, position):
        for i in range(len(self.tables) - 1, -1, -1):
            ObtainedTable = self.tables[i]
            if ObtainedTable.contains(QPoint(position.x(), position.y())):
                return ObtainedTable
        return None

    def checkTableNameUnique(self, tableName):
        for ObtainedTable in self.tables:
            if ObtainedTable.getTableName() == tableName:
                return False
        return True
