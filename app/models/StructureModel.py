class StructureModel:
    def __init__(self, lineThickness, color, fontSize):
        self.__lineThickness = lineThickness
        self.__color = color
        self.__fontSize = fontSize

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
