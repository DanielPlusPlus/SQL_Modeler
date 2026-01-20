from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


class TableContextMenuView(QMenu):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)

    def setupUI(self):
        self.actionCollapseTable = QAction("Collapse/Expand Table", self)
        self.actionEditTable = QAction("Edit Table", self)
        self.actionDeleteTable = QAction("Delete Table", self)

        self.addAction(self.actionCollapseTable)
        self.addAction(self.actionEditTable)
        self.addAction(self.actionDeleteTable)
