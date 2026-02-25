from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QRect

from app.models.TablesModel import TableModel


class TablesView:
    def __init__(self, TablesModel, ParentWindow):
        self.__TablesModel = TablesModel
        self.__ParentWindow = ParentWindow
        self.drawTables()

    def drawTempTable(self, position, width=100, rowsHeight=20, rowsNumber=5):
        CreatedTable = TableModel(position.x(), position.y(), width, rowsHeight, rowsNumber, 0)
        Painter = QPainter(self.__ParentWindow)
        Painter.setPen(QPen(QColor(Qt.GlobalColor.black), CreatedTable.getLineThickness(), Qt.PenStyle.SolidLine))
        self.__drawTable(Painter, CreatedTable)

    def drawTables(self):
        Painter = QPainter(self.__ParentWindow)
        tables = self.__TablesModel.getTables()
        for ObtainedTable in tables:
            Painter.setPen(QPen(QColor(Qt.GlobalColor.black), ObtainedTable.getLineThickness(), Qt.PenStyle.SolidLine))
            if ObtainedTable.getTableCollapseStatus():
                self.__drawCollapsedTable(Painter, ObtainedTable)
            else:
                self.__drawTable(Painter, ObtainedTable)

    def __drawTable(self, Painter, ObtainedTable):
        obtainedTableColumns = ObtainedTable.getTableColumns()
        titleRectangle = ObtainedTable.getTitleRectangle()

        font = QFont("Sans", ObtainedTable.getFontSize())
        font.setBold(True)
        Painter.setFont(font)
        Painter.fillRect(ObtainedTable.getRectangle(), ObtainedTable.getColor())

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

        font = QFont("Sans", ObtainedTable.getFontSize())
        font.setBold(True)
        Painter.setFont(font)
        Painter.fillRect(titleRectangle, ObtainedTable.getColor())

        Painter.drawRect(titleRectangle)
        Painter.drawText(titleRectangle, Qt.AlignCenter, ObtainedTable.getTableName())
