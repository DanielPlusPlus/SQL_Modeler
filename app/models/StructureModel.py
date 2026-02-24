class StructureModel:
    def __init__(self, color):
        self.__color = color

    def getColor(self):
        return self.__color

    def changeColor(self, newColor):
        self.__color = newColor
