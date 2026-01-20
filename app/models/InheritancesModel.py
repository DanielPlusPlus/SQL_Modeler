from PySide6.QtCore import QPoint

from app.models.InheritanceModel import InheritanceModel


class InheritancesModel:
    def __init__(self):
        self.__inheritances = []

    def addInheritance(self, FirstTable, SecondTable):
        CreatedInheritance = InheritanceModel(FirstTable, SecondTable)
        self.__inheritances.append(CreatedInheritance)

    def addInheritanceModel(self, inheritance: InheritanceModel):
        if isinstance(inheritance, InheritanceModel):
            self.__inheritances.append(inheritance)
        else:
            raise TypeError("addInheritanceModel expects an InheritanceModel instance")

    def clearInheritances(self):
        self.__inheritances.clear()

    def getInheritances(self):
        return self.__inheritances

    def deleteSelectedInheritance(self, SelectedInheritance):
        self.__inheritances.remove(SelectedInheritance)

    def deleteInheritanceByTable(self, ObtainedTable):
        self.__inheritances = [
            inheritance for inheritance in self.__inheritances
            if inheritance.getFirstTable() is not ObtainedTable
            and inheritance.getSecondTable() is not ObtainedTable
        ]

    def getInheritanceFromPosition(self, position):
        for ObtainedInheritance in self.__inheritances:
            if ObtainedInheritance.contains(QPoint(position.x(), position.y())):
                return ObtainedInheritance
        return None
