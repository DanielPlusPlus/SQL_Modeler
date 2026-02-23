class TableContextMenuController:
    def __init__(self, TableContextMenuView):
        self.__isChangeTableColorSelected = False
        self.__isCollapseExpandTableSelected = False
        self.__isEditTableSelected = False
        self.__isDeleteTableSelected = False
        TableContextMenuView.actionChangeTableColor.triggered.connect(self.__selectChangeTableColor)
        TableContextMenuView.actionCollapseExpandTable.triggered.connect(self.__selectCollapseExpandTable)
        TableContextMenuView.actionEditTable.triggered.connect(self.__selectEditTable)
        TableContextMenuView.actionDeleteTable.triggered.connect(self.__selectDeleteTable)

    def __selectChangeTableColor(self):
        self.__isChangeTableColorSelected = True

    def unselectChangeTableColor(self):
        self.__isChangeTableColorSelected = False

    def getSelectChangeTableColorStatus(self):
        return self.__isChangeTableColorSelected

    def __selectCollapseExpandTable(self):
        self.__isCollapseExpandTableSelected = True

    def unselectCollapseExpandTable(self):
        self.__isCollapseExpandTableSelected = False

    def getSelectCollapseExpandTableStatus(self):
        return self.__isCollapseExpandTableSelected

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
