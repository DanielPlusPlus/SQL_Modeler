from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction, QIcon


class MenuBarView(QMenuBar):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)
        self.setObjectName(u"MenuBar")

    def setupUI(self):
        self.__menuFile = QMenu(u"File", self)
        self.__menuImportSQL = QMenu(u"Import SQL File", self)
        self.__menuView = QMenu(u"View", self)
        self.__menuTables = QMenu(u"Tables", self)
        self.__menuConnections = QMenu(u"Connections", self)
        self.__menuRelationships = QMenu(u"Relationships", self)
        self.__menuRelationships.setIcon(QIcon("app\\icons\\relationship.png"))

        self.actionImportOracleSQL = QAction(u"Import Oracle SQL File", self)
        self.actionImportMySQL = QAction(u"Import MySQL File", self)
        self.actionImportMSSSQL = QAction(u"Import Microsoft Server SQL File", self)
        self.actionImportPostgreSQL = QAction(u"Import PostgreSQL File", self)

        self.actionExportDiagram = QAction(u"Export Diagram", self)
        self.actionGenerateSQL = QAction(u"Generate SQL Code", self)
        self.actionQuit = QAction(u"Quit", self)

        self.actionZoomIn = QAction(u"Zoom In", self)
        self.actionZoomOut = QAction(u"Zoom Out", self)
        self.actionResetZoom = QAction(u"Reset Zoom", self)

        self.actionCreateTable = QAction(QIcon("app\\icons\\table.png"), u"Create Table", self)

        self.actionCreate_1_1_Rel = QAction(QIcon("app\\icons\\1_1_rel.png"), u"Create 1:1 Relationship", self)
        self.actionCreate_1_n_Rel = QAction(QIcon("app\\icons\\1_n_rel.png"), u"Create 1:n Relationship", self)
        self.actionCreate_n_n_Rel = QAction(QIcon("app\\icons\\n_n_rel.png"), u"Create n:n Relationship", self)

        self.actionCreateInheritance = QAction(QIcon("app\\icons\\inheritance.png"),
                                               u"Create Inheritance Relationship", self)

        self.__menuFile.addMenu(self.__menuImportSQL)
        self.__menuImportSQL.addAction(self.actionImportOracleSQL)
        self.__menuImportSQL.addAction(self.actionImportMySQL)
        self.__menuImportSQL.addAction(self.actionImportMSSSQL)
        self.__menuImportSQL.addAction(self.actionImportPostgreSQL)
        self.__menuFile.addAction(self.actionExportDiagram)
        self.__menuFile.addAction(self.actionGenerateSQL)
        self.__menuFile.addAction(self.actionQuit)

        self.__menuView.addAction(self.actionZoomIn)
        self.__menuView.addAction(self.actionZoomOut)
        self.__menuView.addAction(self.actionResetZoom)

        self.__menuTables.addAction(self.actionCreateTable)

        self.__menuConnections.addMenu(self.__menuRelationships)
        self.__menuRelationships.addAction(self.actionCreate_1_1_Rel)
        self.__menuRelationships.addAction(self.actionCreate_1_n_Rel)
        self.__menuRelationships.addAction(self.actionCreate_n_n_Rel)
        self.__menuConnections.addAction(self.actionCreateInheritance)

        self.addMenu(self.__menuFile)
        self.addMenu(self.__menuView)
        self.addMenu(self.__menuTables)
        self.addMenu(self.__menuConnections)
