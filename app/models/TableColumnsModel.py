from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from typing import override


class TableColumnsModel(QAbstractTableModel):
    def __init__(self, columns=None):
        super().__init__()
        self.__columns = columns or []
        self.isEditColumnsSelected = False

    @override
    def rowCount(self, parent=QModelIndex()):
        return len(self.__columns)

    @override
    def columnCount(self, parent=QModelIndex):
        return 7

    @override
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role in (Qt.DisplayRole, Qt.EditRole):
            if column == 0:
                return self.__columns[row]["columnName"]
            elif column == 1:
                return self.__columns[row]["dataType"]
            elif column == 2:
                return "DEFAULT" if self.__columns[row]["length"] == 0 else self.__columns[row]["length"]
            elif column in (3, 4, 5, 6):
                return ""

        if role == Qt.CheckStateRole:
            if column == 3:
                return Qt.Checked if self.__columns[row]["unique"] else Qt.Unchecked
            elif column == 4:
                return Qt.Checked if self.__columns[row]["notNull"] else Qt.Unchecked
            elif column == 5:
                return Qt.Checked if self.__columns[row]["pk"] else Qt.Unchecked
            elif column == 6:
                return Qt.Checked if self.__columns[row]["fk"] else Qt.Unchecked

        return None

    @override
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        baseFlags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if self.isEditColumnsSelected:
            if index.column() in (0, 1, 2):
                return baseFlags | Qt.ItemIsEditable
            if index.column() in (3, 4, 5):
                return baseFlags | Qt.ItemIsUserCheckable
            if index.column() == 6:
                return baseFlags
        else:
            return baseFlags

    @override
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role == Qt.EditRole:
            if column == 0:
                self.__columns[row]["columnName"] = value
            elif column == 1:
                self.__columns[row]["dataType"] = value
            elif column == 2:
                self.__columns[row]["length"] = value
            self.dataChanged.emit(index, index)
            return True

        if role == Qt.CheckStateRole:
            value = Qt.CheckState(value)
            if column == 3:
                self.__columns[row]["unique"] = (value == Qt.Checked)
            elif column == 4:
                self.__columns[row]["notNull"] = (value == Qt.Checked)
            elif column == 5:
                self.__columns[row]["pk"] = (value == Qt.Checked)
            elif column == 6:
                self.__columns[row]["fk"] = (value == Qt.Checked)
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole, Qt.CheckStateRole])
            return True

        return False

    @override
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            headers = ["Column Name", "Type", "Length", "UNIQUE", "NOT NULL", "PK", "FK"]
            return headers[section]

        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None

    def __emitAllDataChanges(self):
        topLeft = self.index(0, 0)
        bottomRight = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(topLeft, bottomRight, [Qt.DisplayRole, Qt.EditRole, Qt.CheckStateRole])

    def addColumn(self, columnName, dataType, length, unique=False, notNull=False, pk=False, fk=False):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.__columns.append({"columnName": columnName, "dataType": dataType, "length": length, "unique": unique,
                               "notNull": notNull, "pk": pk, "fk": fk})
        self.endInsertRows()

    def deleteColumn(self, row):
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.__columns[row]
            self.endRemoveRows()

    def setForeignKeyByColumnName(self, columnName):
        for column in self.__columns:
            if column.get("columnName") == columnName:
                if column.get("pk") or column.get("unique"):
                    return False
                column["fk"] = True
                return True
        return False

    def toggleEditColumns(self):
        self.isEditColumnsSelected = not self.isEditColumnsSelected
        self.__emitAllDataChanges()

    def getColumns(self):
        return self.__columns

    def getEditColumnsStatus(self):
        return self.isEditColumnsSelected
