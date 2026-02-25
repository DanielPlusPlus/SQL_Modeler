class DrawingAreaModel:
    def __init__(self):
        self.__START_MINIMUM_WIDTH = 400
        self.__START_MINIMUM_HEIGHT = 400
        self.__START_MAXIMUM_WIDTH = 800
        self.__START_MAXIMUM_HEIGHT = 600
        self.__DIMENSIONS_OFFSET = 50
        self.__actualMinimumWidth = self.__START_MINIMUM_WIDTH
        self.__actualMinimumHeight = self.__START_MINIMUM_HEIGHT
        self.__actualMaximumWidth = self.__START_MAXIMUM_WIDTH
        self.__actualMaximumHeight = self.__START_MAXIMUM_HEIGHT
        self.__scaleFactor = 1.0

    def getStartMinimumWidth(self):
        return self.__START_MINIMUM_WIDTH

    def getStartMinimumHeight(self):
        return self.__START_MINIMUM_HEIGHT

    def getStartMaximumWidth(self):
        return self.__START_MAXIMUM_WIDTH

    def getStartMaximumHeight(self):
        return self.__START_MAXIMUM_HEIGHT

    def getActualMinimumWidth(self):
        return self.__actualMinimumWidth

    def getActualMinimumHeight(self):
        return self.__actualMinimumHeight

    def getActualMaximumWidth(self):
        return self.__actualMaximumWidth

    def getActualMaximumHeight(self):
        return self.__actualMaximumHeight

    def getScaleFactor(self):
        return self.__scaleFactor

    def changeMinimumDimensions(self, extremeTableRightDimension, extremeTableBottomDimension):
        self.__actualMinimumWidth = max(self.__START_MINIMUM_WIDTH,
                                        extremeTableRightDimension + self.__DIMENSIONS_OFFSET)
        self.__actualMinimumHeight = max(self.__START_MINIMUM_HEIGHT,
                                         extremeTableBottomDimension + self.__DIMENSIONS_OFFSET)

    def changeMaximumDimensions(self, extremeTableRightDimension, extremeTableBottomDimension):
        self.__actualMaximumWidth = max(self.__START_MAXIMUM_WIDTH,
                                        extremeTableRightDimension + self.__DIMENSIONS_OFFSET)
        self.__actualMaximumHeight = max(self.__START_MAXIMUM_HEIGHT,
                                         extremeTableBottomDimension + self.__DIMENSIONS_OFFSET)

    def increaseScaleFactor(self):
        self.__scaleFactor = min(2.0, round(self.__scaleFactor + 0.1, 1))

    def decreaseScaleFactor(self):
        self.__scaleFactor = max(0.1, round(self.__scaleFactor - 0.1, 1))

    def resetScaleFactor(self):
        self.__scaleFactor = 1.0
