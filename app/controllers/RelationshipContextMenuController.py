class RelationshipContextMenuController:
    def __init__(self, RelationshipContextMenuView):
        self.__isDeleteRelationshipSelected = False
        RelationshipContextMenuView.actionDeleteRelationship.triggered.connect(self.__selectDeleteRelationship)

    def __selectDeleteRelationship(self):
        self.__isDeleteRelationshipSelected = True

    def unselectDeleteRelationship(self):
        self.__isDeleteRelationshipSelected = False

    def getSelectDeleteRelationshipStatus(self):
        return self.__isDeleteRelationshipSelected
