from PySide6.QtCore import QPoint

from app.models.RelationshipModel import RelationshipModel
from app.enums.RelationshipsEnum import RelationshipsEnum


class RelationshipsModel:
    def __init__(self):
        self.__relationships = []

    def add_1_1_Relationship(self, FirstTable, SecondTable, firstSelectedColumnName, secondSelectedColumnName):
        CreatedRelationship = RelationshipModel(
            FirstTable,
            SecondTable,
            firstSelectedColumnName,
            secondSelectedColumnName,
            RelationshipsEnum.REL_1_1
        )
        self.__relationships.append(CreatedRelationship)

    def add_1_n_Relationship(self, FirstTable, SecondTable, firstSelectedColumnName, secondSelectedColumnName):
        CreatedRelationship = RelationshipModel(
            FirstTable,
            SecondTable,
            firstSelectedColumnName,
            secondSelectedColumnName,
            RelationshipsEnum.REL_1_n
        )
        self.__relationships.append(CreatedRelationship)

    def add_n_n_Relationship(self, FirstTable, SecondTable, firstSelectedColumnName, secondSelectedColumnName):
        CreatedRelationship = RelationshipModel(
            FirstTable,
            SecondTable,
            firstSelectedColumnName,
            secondSelectedColumnName,
            RelationshipsEnum.REL_n_n
        )
        self.__relationships.append(CreatedRelationship)

    def addRelationship(self, relationship: RelationshipModel):
        if isinstance(relationship, RelationshipModel):
            self.__relationships.append(relationship)
        else:
            raise TypeError("addRelationship expects a RelationshipModel instance")

    def clearRelationships(self):  # deprecated
        self.__relationships.clear()

    def getRelationships(self):
        return self.__relationships

    def deleteSelectedRelationship(self, SelectedRelationship):
        self.__relationships.remove(SelectedRelationship)

    def deleteRelationshipByTable(self, ObtainedTable):
        self.__relationships = [
            relationship for relationship in self.__relationships
            if relationship.getFirstTable() is not ObtainedTable
            and relationship.getSecondTable() is not ObtainedTable
        ]

    def getRelationshipFromPosition(self, position):
        for ObtainedRelationship in self.__relationships:
            if ObtainedRelationship.contains(QPoint(position.x(), position.y())):
                return ObtainedRelationship
        return None
