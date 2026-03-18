from PySide6.QtWidgets import QTabWidget

from app.views.widgets.CodeEditor import CodeEditor


class TabWidget(QTabWidget):
    def __init__(self, SQLCode, ParentWindow=None):
        super().__init__(ParentWindow)
        self.__SQLCode = SQLCode
        self.__tabsLabels = (u"Oracle SQL", u"MySQL", u"Microsoft Server SQL", u"PostgreSQL")
        self.addTabs()

    def addTabs(self):
        for label in self.__tabsLabels:
            SQLCodeTextEdit = CodeEditor(self)
            SQLCodeTextEdit.setReadOnly(True)
            SQLCodeTextEdit.setPlainText(self.__SQLCode)
            self.addTab(SQLCodeTextEdit, label)
