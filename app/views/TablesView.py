from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QRect

from app.models.TablesModel import TableModel


class TablesView:
    def __init__(self, TablesModel, ParentWindow):
        self.__TablesModel = TablesModel
        self.__ParentWindow = ParentWindow
        self.drawTables()

    def drawTempTable(self, position, width=100, rowsHeight=20, rowsNumber=5):
        Painter = QPainter(self.__ParentWindow)
        Painter.setPen(QPen(QColor(Qt.GlobalColor.black), 2, Qt.PenStyle.SolidLine))
        CreatedTable = TableModel(position.x(), position.y(), width, rowsHeight, rowsNumber, 0)
        self.__drawTable(Painter, CreatedTable)

    def drawTables(self):
        Painter = QPainter(self.__ParentWindow)
        Painter.setPen(QPen(QColor(Qt.GlobalColor.black), 2, Qt.PenStyle.SolidLine))
        tables = self.__TablesModel.getTables()
        for ObtainedTable in tables:
            if ObtainedTable.getTableCollapseStatus():
                self.__drawCollapsedTable(Painter, ObtainedTable)
            else:
                self.__drawTable(Painter, ObtainedTable)

    def __drawTable(self, Painter, ObtainedTable):
        obtainedTableColumns = ObtainedTable.getTableColumns()
        titleRectangle = ObtainedTable.getTitleRectangle()

        font = QFont("Sans", 10)
        font.setBold(True)
        Painter.setFont(font)
        backgroundColor = ObtainedTable.getColor()
        Painter.fillRect(ObtainedTable.getRectangle(), backgroundColor)

        Painter.drawText(titleRectangle, Qt.AlignCenter, ObtainedTable.getTableName())

        for row in range(ObtainedTable.getRowsNumber()):
            y = ObtainedTable.getTop() + row * ObtainedTable.getRowHeight()
            rowRectangle = QRect(ObtainedTable.getLeft(), y, ObtainedTable.getTableWidth(),
                                 ObtainedTable.getRowHeight())
            Painter.drawRect(rowRectangle)
            if row < len(obtainedTableColumns):
                Painter.drawText(rowRectangle, Qt.AlignCenter, f"{obtainedTableColumns[row]["columnName"]}")
        Painter.drawRect(ObtainedTable.getRectangle())

    def __drawCollapsedTable(self, Painter, ObtainedTable):
        titleRectangle = ObtainedTable.getTitleRectangle()

        font = QFont("Sans", 10)
        font.setBold(True)
        Painter.setFont(font)
        backgroundColor = ObtainedTable.getColor()
        Painter.fillRect(titleRectangle, backgroundColor)

        Painter.drawRect(titleRectangle)
        Painter.drawText(titleRectangle, Qt.AlignCenter, ObtainedTable.getTableName())
