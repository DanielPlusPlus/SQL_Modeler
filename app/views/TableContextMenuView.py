from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


class TableContextMenuView(QMenu):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)

    def setupUI(self, tableCollapseStatus):
        self.actionChangeTableColor = QAction(u"Change Color", self)
        self.actionCollapseExpandTable = QAction(u"Collapse/Expand Table", self)
        if tableCollapseStatus:
            self.actionCollapseExpandTable.setText(u"Expand Table")
        else:
            self.actionCollapseExpandTable.setText(u"Collapse Table")
        self.actionEditTable = QAction(u"Edit Table", self)
        self.actionDeleteTable = QAction(u"Delete Table", self)

        self.addAction(self.actionChangeTableColor)
        self.addAction(self.actionCollapseExpandTable)
        self.addAction(self.actionEditTable)
        self.addAction(self.actionDeleteTable)

    def display(self, globalCursorPosition):
        self.exec(globalCursorPosition)
