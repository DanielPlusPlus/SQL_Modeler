from PySide6.QtWidgets import QTabWidget

from app.views.widgets.CodeEditor import CodeEditor


class TabWidget(QTabWidget):
    def __init__(self, oracleSQLCode, mySQLCode, msSQLCode, postgreSQLCode, ParentWindow=None):
        super().__init__(ParentWindow)
        self.__tabsCodes = (oracleSQLCode, mySQLCode, msSQLCode, postgreSQLCode)
        self.__tabsLabels = (u"Oracle SQL", u"MySQL", u"Microsoft Server SQL", u"PostgreSQL")
        self.addTabs()

    def addTabs(self):
        for i in range(len(self.__tabsLabels)):
            SQLCodeTextEdit = CodeEditor(self)
            SQLCodeTextEdit.setReadOnly(True)
            SQLCodeTextEdit.setPlainText(self.__tabsCodes[i])
            self.addTab(SQLCodeTextEdit, self.__tabsLabels[i])
