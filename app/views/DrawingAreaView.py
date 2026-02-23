from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt
from typing import override


class DrawingAreaView(QWidget):
    def __init__(self, DrawingAreaController, DrawingAreaModel):
        super().__init__()
        self.__DrawingAreaController = DrawingAreaController
        self.__DrawingAreaModel = DrawingAreaModel
        self.setMinimumSize(self.__DrawingAreaModel.getStartMinimumWidth(),
                            self.__DrawingAreaModel.getStartMinimumHeight())
        self.setMaximumSize(self.__DrawingAreaModel.getStartMaximumWidth(),
                            self.__DrawingAreaModel.getStartMaximumHeight())
        self.setMouseTracking(True)

    def setupUI(self):
        self.setObjectName(u"DrawingArea")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #E6E6E6;")

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

