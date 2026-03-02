class StructureModel:
    def __init__(self, lineThickness, fontSize, color):
        self.__baseLineThickness = lineThickness
        self.__baseFontSize = fontSize
        self.__lineThickness = self.__baseLineThickness
        self.__fontSize = self.__baseFontSize
        self.__color = color

    def getLineThickness(self):
        return self.__lineThickness

    def changeLineThickness(self, newLineThickness):
        self.__lineThickness = newLineThickness

    def getColor(self):
        return self.__color

    def changeColor(self, newColor):
        self.__color = newColor

    def getFontSize(self):
        return self.__fontSize

    def changeFontSize(self, newFontSize):
        self.__fontSize = newFontSize

    def scaleStructureDimensions(self, scaleFactor):
        self.__lineThickness = max(1, int(self.__baseLineThickness * scaleFactor))
        self.__fontSize = max(1, int(self.__baseFontSize * scaleFactor))
