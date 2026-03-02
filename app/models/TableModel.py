from PySide6.QtCore import QRect
from PySide6.QtGui import QColor

from app.models.StructureModel import StructureModel
from app.models.TableColumnsModel import TableColumnsModel


class TableModel(StructureModel):
    def __init__(self, x, y, scaleFactor, width, rowHeight, minRowsNumber, tableNumber):
        super().__init__(2, 10, QColor("#FFFF99"))
        self.__BaseRectangle = QRect(
            x - width // 2,
            y - (rowHeight * minRowsNumber) // 2,
            width,
            rowHeight * minRowsNumber
        )
        self.__Rectangle = self.__BaseRectangle
        self.__baseTableWidth = width
        self.__baseRowHeight = rowHeight
        self.__tableWidth = self.__baseTableWidth
        self.__rowHeight = self.__baseRowHeight
        self.__minRowsNumber = minRowsNumber
        self.__rowsNumber = minRowsNumber
        self.__tableNumber = tableNumber
        self.__isTableCollapsed = False
        if not self.__tableNumber:
            self.__tableName = "New Table"
        else:
            self.__tableName = f"Table {tableNumber}"
        self.__TableColumnsModel = TableColumnsModel()
        self.scaleTableDimensions(scaleFactor)
        self.changeTablePosition(x, y, scaleFactor)

    def getRectangle(self):
        return self.__Rectangle

    def __getBaseTop(self):
        return self.__BaseRectangle.top()

    def __getBaseLeft(self):
        return self.__BaseRectangle.left()

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

    def getTableCollapseStatus(self):
        return self.__isTableCollapsed

    def editTableName(self, newName):
        self.__tableName = newName

    def __changeBaseTop(self, newTop):
        self.__BaseRectangle.moveTop(newTop)

    def __changeBaseLeft(self, newLeft):
        return self.__BaseRectangle.moveLeft(newLeft)

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

    def changeTablePosition(self, x, y, scaleFactor):
        if self.__isTableCollapsed:
            newTop = y + self.getRowHeight() // 2
        else:
            newTop = y - (self.getRowHeight() * self.getRowsNumber()) // 2
        newLeft = x - self.getTableWidth() // 2

        self.__Rectangle = QRect(
            newLeft,
            newTop,
            self.getTableWidth(),
            self.__rowHeight * self.getRowsNumber()
        )

        self.__changeBaseLeft(newLeft / scaleFactor)
        self.__changeBaseTop(newTop / scaleFactor)

    def scaleTableDimensions(self, scaleFactor):
        scaledWidth = int(self.__baseTableWidth * scaleFactor)
        scaledRowHeight = int(self.__baseRowHeight * scaleFactor)
        scaledLeft = int(self.__getBaseLeft() * scaleFactor)
        scaledTop = int(self.__getBaseTop() * scaleFactor)

        self.__tableWidth = scaledWidth
        self.__rowHeight = scaledRowHeight

        self.__Rectangle = QRect(
            scaledLeft,
            scaledTop,
            scaledWidth,
            scaledRowHeight * self.__rowsNumber
        )

        self.scaleStructureDimensions(scaleFactor)

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


