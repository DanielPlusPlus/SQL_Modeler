class DrawingAreaModel:
    def __init__(self):
        self.__baseMinimumWidth = 400
        self.__baseMinimumHeight = 400
        self.__baseMaximumWidth = 800
        self.__baseMaximumHeight = 600
        self.__DimensionsOffset = 50
        self.__actualMinimumWidth = self.__baseMinimumWidth
        self.__actualMinimumHeight = self.__baseMinimumHeight
        self.__actualMaximumWidth = self.__baseMaximumWidth
        self.__actualMaximumHeight = self.__baseMaximumHeight
        self.__scaleFactor = 1.0

    def getBaseMinimumWidth(self):
        return self.__baseMinimumWidth

    def getBaseMinimumHeight(self):
        return self.__baseMinimumHeight

    def getBaseMaximumWidth(self):
        return self.__baseMaximumWidth

    def getBaseMaximumHeight(self):
        return self.__baseMaximumHeight

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
        self.__actualMinimumWidth = max(self.__baseMinimumWidth,
                                        extremeTableRightDimension + self.__DimensionsOffset)
        self.__actualMinimumHeight = max(self.__baseMinimumHeight,
                                         extremeTableBottomDimension + self.__DimensionsOffset)

    def changeMaximumDimensions(self, extremeTableRightDimension, extremeTableBottomDimension):
        self.__actualMaximumWidth = max(self.__baseMaximumWidth,
                                        extremeTableRightDimension + self.__DimensionsOffset)
        self.__actualMaximumHeight = max(self.__baseMaximumHeight,
                                         extremeTableBottomDimension + self.__DimensionsOffset)

    def increaseScaleFactor(self):
        self.__scaleFactor = min(2.0, round(self.__scaleFactor + 0.1, 1))

    def decreaseScaleFactor(self):
        self.__scaleFactor = max(0.1, round(self.__scaleFactor - 0.1, 1))

    def resetScaleFactor(self):
        self.__scaleFactor = 1.0
