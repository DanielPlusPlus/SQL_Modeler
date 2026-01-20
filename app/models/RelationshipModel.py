from app.models.ConnectionModel import ConnectionModel


class RelationshipModel(ConnectionModel):
    def __init__(self, FirstTable, SecondTable, firstSelectedColumnName, secondSelectedColumnName, relationshipType):
        super().__init__(FirstTable, SecondTable)
        self.__firstSelectedColumnName = firstSelectedColumnName
        self.__secondSelectedColumnName = secondSelectedColumnName
        self.__relationshipType = relationshipType

    def getFirstSelectedColumnName(self):
        return self.__firstSelectedColumnName

    def getSecondSelectedColumnName(self):
        return self.__secondSelectedColumnName

    def getRelationshipType(self):
        return self.__relationshipType

