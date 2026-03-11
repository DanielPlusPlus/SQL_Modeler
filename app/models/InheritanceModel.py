from app.models.ConnectionModel import ConnectionModel


class InheritanceModel(ConnectionModel):
    def __init__(self, FirstTable, SecondTable, scaleFactor):
        super().__init__(FirstTable, SecondTable)
        self.scaleStructureDimensions(scaleFactor)
