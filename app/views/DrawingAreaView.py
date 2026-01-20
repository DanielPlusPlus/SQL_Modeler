from PySide6.QtWidgets import QWidget
from typing import override


class DrawingAreaView(QWidget):
    def __init__(self, DrawingAreaController):
        super().__init__()
        self.setMinimumSize(3840, 2160)
        self.__DrawingAreaController = DrawingAreaController
        self.__TablesModel = None
        self.__TableController = None
        self.setMouseTracking(True)

    def setupUI(self):
        self.setObjectName(u"DrawingArea")

    def setTablesModel(self, TablesModel):
        self.__TablesModel = TablesModel

    @override
    def mouseMoveEvent(self, event):
        self.__DrawingAreaController.handleMouseMove(event)
        self.update()

    @override
    def mousePressEvent(self, event):
        self.__DrawingAreaController.handleMousePress(event)
        self.update()

    @override
    def paintEvent(self, event):
        self.__DrawingAreaController.handlePaintEvent()
