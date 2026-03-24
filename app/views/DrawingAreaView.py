from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt
from typing import override


class DrawingAreaView(QWidget):
    def __init__(self, DrawingAreaController, DrawingAreaModel):
        super().__init__()
        self.__DrawingAreaController = DrawingAreaController
        self.__DrawingAreaModel = DrawingAreaModel
        self.setMinimumSize(self.__DrawingAreaModel.getBaseMinimumWidth(),
                            self.__DrawingAreaModel.getBaseMinimumHeight())
        self.setMaximumSize(self.__DrawingAreaModel.getBaseMaximumWidth(),
                            self.__DrawingAreaModel.getBaseMaximumHeight())
        self.setMouseTracking(True)

    def setupUI(self):
        self.setObjectName(u"DrawingArea")
        self.setAttribute(Qt.WA_StyledBackground, True)

    @override
    def mouseMoveEvent(self, event):
        self.__DrawingAreaController.handleMouseMove(event)
        self.update()

    @override
    def mousePressEvent(self, event):
        self.__DrawingAreaController.handleMousePress(event)
        self.update()

    @override
    def wheelEvent(self, event):
        self.__DrawingAreaController.handleWheelMove(event)
        self.update()

    @override
    def paintEvent(self, event):
        self.__DrawingAreaController.handlePaintEvent()

