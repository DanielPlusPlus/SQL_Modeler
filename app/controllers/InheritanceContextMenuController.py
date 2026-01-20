class InheritanceContextMenuController:
    def __init__(self, InheritanceContextMenuView):
        self.__isDeleteInheritanceSelected = False
        InheritanceContextMenuView.actionDeleteInheritance.triggered.connect(self.__selectDeleteInheritance)

    def __selectDeleteInheritance(self):
        self.__isDeleteInheritanceSelected = True

    def unselectDeleteInheritance(self):
        self.__isDeleteInheritanceSelected = False

    def getSelectDeleteInheritanceStatus(self):
        return self.__isDeleteInheritanceSelected
