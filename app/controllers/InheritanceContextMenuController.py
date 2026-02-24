class InheritanceContextMenuController:
    def __init__(self, InheritanceContextMenuView):
        self.__isChangeInheritanceColorSelected = False
        self.__isDeleteInheritanceSelected = False
        InheritanceContextMenuView.actionChangeInheritanceColor.triggered.connect(self.__selectChangeInheritanceColor)
        InheritanceContextMenuView.actionDeleteInheritance.triggered.connect(self.__selectDeleteInheritance)

    def __selectChangeInheritanceColor(self):
        self.__isChangeInheritanceColorSelected = True

    def unselectChangeInheritanceColor(self):
        self.__isChangeInheritanceColorSelected = False

    def getSelectChangeInheritanceColorStatus(self):
        return self.__isChangeInheritanceColorSelected

    def __selectDeleteInheritance(self):
        self.__isDeleteInheritanceSelected = True

    def unselectDeleteInheritance(self):
        self.__isDeleteInheritanceSelected = False

    def getSelectDeleteInheritanceStatus(self):
        return self.__isDeleteInheritanceSelected
