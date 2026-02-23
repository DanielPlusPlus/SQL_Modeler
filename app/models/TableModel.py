from PySide6.QtCore import QRect
from PySide6.QtGui import QColor

from app.models.TableColumnsModel import TableColumnsModel


class TableModel:
    def __init__(self, x, y, width, rowHeight, minRowsNumber, tableNumber):
        self.__Rectangle = QRect(
            x - width // 2,
            y - (rowHeight * minRowsNumber) // 2,
            width,
            rowHeight * minRowsNumber
        )
        self.__tableWidth = width
        self.__rowHeight = rowHeight
        self.__minRowsNumber = minRowsNumber
        self.__rowsNumber = minRowsNumber
        self.__tableNumber = tableNumber
        self.__tableColor = QColor("#FFFF99")
        self.__isTableCollapsed = False
        if not self.__tableNumber:
            self.__tableName = "New Table"
        else:
            self.__tableName = f"Table {tableNumber}"
        self.__TableColumnsModel = TableColumnsModel()

    def getRectangle(self):
        return self.__Rectangle

    def getTop(self):
        return self.__Rectangle.top()

    def getLeft(self):
        return self.__Rectangle.left()

    def getRight(self):
        return self.__Rectangle.right()

    def getBottom(self):
        return self.__Rectangle.bottom()

    def getTableWidth(self):
        return self.__tableWidth

    def getRowHeight(self):
        return self.__rowHeight

    def getRowsNumber(self):
        return self.__rowsNumber

    def getTableNumber(self):
        return self.__tableNumber

    def getTableName(self):
        return self.__tableName

    def getTableColumnsModel(self):
        return self.__TableColumnsModel

    def getTableColumns(self):
        return self.__TableColumnsModel.getColumns()

    def getTitleRectangle(self):
        return QRect(
            self.getLeft(),
            self.getTop() - self.getRowHeight(),
            self.getTableWidth(),
            self.getRowHeight()
        )

    def getTableColor(self):
        return self.__tableColor

    def getTableCollapseStatus(self):
        return self.__isTableCollapsed

    def editTableName(self, newName):
        self.__tableName = newName

    def changeTableDimensions(self):
        self.__rowsNumber = max(self.__minRowsNumber, self.__TableColumnsModel.rowCount())
        self.__Rectangle = QRect(
            self.getLeft(),
            self.getTop(),
            self.__tableWidth,
            self.__rowsNumber * self.__rowHeight
        )

    def changeTableColumnsModel(self, NewTableColumnsModel):
        self.__TableColumnsModel = NewTableColumnsModel

    def changeTablePosition(self, x, y):
        if self.__isTableCollapsed:
            yPos = y + self.getRowHeight() // 2
        else:
            yPos = y - (self.getRowHeight() * self.getRowsNumber()) // 2

        newRectangle = QRect(
            x - self.getTableWidth() // 2,
            yPos,
            self.getTableWidth(),
            self.__rowHeight * self.getRowsNumber()
        )
        self.__Rectangle = newRectangle

    def changeTableColor(self, newColor):
        self.__tableColor = newColor

    def changeTableCollapseStatus(self):
        self.__isTableCollapsed = not self.__isTableCollapsed

    def contains(self, point):
        if self.__isTableCollapsed:
            if self.getTitleRectangle().contains(point):
                return True
        else:
            if self.__Rectangle.contains(point):
                return True
        return False
