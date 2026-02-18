from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt
from typing import override


class DrawingAreaView(QWidget):
    def __init__(self, DrawingAreaController):
        super().__init__()
        # do modelu
        self.__minimumWidth = 400
        self.__minimumHeight = 400
        self.__DrawingAreaController = DrawingAreaController
        self.setMinimumSize(self.__minimumWidth, self.__minimumHeight)
        self.setMaximumSize(800, 600)
        self.setMouseTracking(True)
        self.scale_factor = 1.0

    def setupUI(self):
        self.setObjectName(u"DrawingArea")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #e6e6e6;")

    def getMinimumWidth(self):
        return self.__minimumWidth

    def getMinimumHeight(self):
        return self.__minimumHeight

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

