from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


class RelationshipContextMenuView(QMenu):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)

    def setupUI(self):
        self.actionChangeRelationshipColor = QAction(u"Change Color", self)
        self.actionDeleteRelationship = QAction(u"Delete Relationship", self)

        self.addAction(self.actionChangeRelationshipColor)
        self.addAction(self.actionDeleteRelationship)

    def display(self, globalCursorPosition):
        self.exec(globalCursorPosition)

