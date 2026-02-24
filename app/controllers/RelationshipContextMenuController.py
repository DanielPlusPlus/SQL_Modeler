class RelationshipContextMenuController:
    def __init__(self, RelationshipContextMenuView):
        self.__isChangeRelationshipColorSelected = False
        self.__isDeleteRelationshipSelected = False
        RelationshipContextMenuView.actionChangeRelationshipColor.triggered.connect(self.__selectChangeRelationshipColor)
        RelationshipContextMenuView.actionDeleteRelationship.triggered.connect(self.__selectDeleteRelationship)

    def __selectChangeRelationshipColor(self):
        self.__isChangeRelationshipColorSelected = True

    def unselectChangeRelationshipColor(self):
        self.__isChangeRelationshipColorSelected = False

    def getSelectChangeRelationshipColorStatus(self):
        return self.__isChangeRelationshipColorSelected

    def __selectDeleteRelationship(self):
        self.__isDeleteRelationshipSelected = True

    def unselectDeleteRelationship(self):
        self.__isDeleteRelationshipSelected = False

    def getSelectDeleteRelationshipStatus(self):
        return self.__isDeleteRelationshipSelected
