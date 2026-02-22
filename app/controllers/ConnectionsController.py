class ConnectionsController:
    def __init__(self, ParentWindow, TablesModel):
        self._ParentWindow = ParentWindow
        self.__TablesModel = TablesModel
        self._FirstClickedTable = None
        self._SecondClickedTable = None

    def setFirstClickedTable(self, cursorPosition):
        ObtainedTable = self.__TablesModel.getTableFromPosition(cursorPosition)

        if ObtainedTable is not None:
            self._FirstClickedTable = ObtainedTable
            return True
        return False

    def setSecondClickedTable(self, cursorPosition):
        ObtainedTable = self.__TablesModel.getTableFromPosition(cursorPosition)

        if ObtainedTable is not None:
            self._SecondClickedTable = ObtainedTable
            return True
        return False

    def resetTables(self):
        self._FirstClickedTable = None
        self._SecondClickedTable = None
