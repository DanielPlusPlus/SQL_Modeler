class DrawingAreaModel:
    def __init__(self):
        self.__START_MINIMUM_WIDTH = 400
        self.__START_MINIMUM_HEIGHT = 400
        self.__START_MAXIMUM_WIDTH = 800
        self.__START_MAXIMUM_HEIGHT = 600
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

    def changeMinimumDimensions(self, newWidth, newHeight):
        self.__actualMinimumWidth = newWidth
        self.__actualMinimumHeight = newHeight

    def changeMaximumDimensions(self, newWidth, newHeight):
        self.__actualMaximumWidth = newWidth
        self.__actualMaximumHeight = newHeight

    def changeScaleFactor(self, newScaleFactor):
        self.__scaleFactor = newScaleFactor
