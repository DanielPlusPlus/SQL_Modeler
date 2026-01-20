from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


class InheritanceContextMenuView(QMenu):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)

    def setupUI(self):
        self.actionDeleteInheritance = QAction("Delete Inheritance", self)
        self.addAction(self.actionDeleteInheritance)
