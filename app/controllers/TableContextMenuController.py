class TableContextMenuController:
    def __init__(self, TableContextMenuView):
        self.__isCollapseTableSelected = False
        self.__isEditTableSelected = False
        self.__isDeleteTableSelected = False
        TableContextMenuView.actionCollapseTable.triggered.connect(self.__selectCollapseTable)
        TableContextMenuView.actionEditTable.triggered.connect(self.__selectEditTable)
        TableContextMenuView.actionDeleteTable.triggered.connect(self.__selectDeleteTable)

    def __selectCollapseTable(self):
        self.__isCollapseTableSelected = True

    def unselectCollapseTable(self):
        self.__isCollapseTableSelected = False

    def getSelectCollapseTableStatus(self):
        return self.__isCollapseTableSelected

    def __selectEditTable(self):
        self.__isEditTableSelected = True

    def unselectEditTable(self):
        self.__isEditTableSelected = False

    def getSelectEditTableStatus(self):
        return self.__isEditTableSelected

    def __selectDeleteTable(self):
        self.__isDeleteTableSelected = True

    def unselectDeleteTable(self):
        self.__isDeleteTableSelected = False

    def getSelectDeleteTableStatus(self):
        return self.__isDeleteTableSelected
