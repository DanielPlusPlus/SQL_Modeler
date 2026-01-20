import sys
import unittest

from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu
from PySide6.QtGui import QAction, Qt

from app.views.MenuBarView import MenuBarView

app = QApplication.instance() or QApplication(sys.argv)


class TestMenuBarView(unittest.TestCase):
    def setUp(self):
        self.window = QMainWindow()
        self.menuBar = MenuBarView(self.window)
        self.window.setMenuBar(self.menuBar)
        self.menuBar.setupUI()

    def test_inherits_qmenubar_and_object_name(self):
        self.assertIsInstance(self.menuBar, QMenuBar)
        self.assertEqual(self.menuBar.objectName(), "MenuBar")

    def test_menus_created_and_added(self):
        top_menus = self.menuBar.findChildren(QMenu, options=Qt.FindDirectChildrenOnly)
        titles = [m.title() for m in top_menus]

        self.assertIn("File", titles)
        self.assertIn("Tables", titles)
        self.assertIn("Connections", titles)

    def test_file_menu_actions(self):
        file_menu = next(m for m in self.menuBar.findChildren(QMenu) if m.title() == "File")
        actions = file_menu.actions()
        texts = [a.text() for a in actions]

        self.assertIn("Import SQL File", texts)
        self.assertIn("Export Diagram", texts)
        self.assertIn("Generate SQL Code", texts)
        self.assertIn("Quit", texts)

        for action in actions:
            self.assertIsInstance(action, QAction)

    def test_tables_menu_actions(self):
        tables_menu = next(m for m in self.menuBar.findChildren(QMenu) if m.title() == "Tables")
        actions = tables_menu.actions()
        texts = [a.text() for a in actions]

        self.assertIn("Create Table", texts)
        for action in actions:
            self.assertIsInstance(action, QAction)

    def test_connections_menu_and_relationships_submenu(self):
        connections_menu = next(m for m in self.menuBar.findChildren(QMenu) if m.title() == "Connections")

        relationships_menu = None
        for action in connections_menu.actions():
            submenu = action.menu()
            if submenu and submenu.title() == "Relationships":
                relationships_menu = submenu
                break

        self.assertIsNotNone(relationships_menu)

        rel_actions = relationships_menu.actions()
        rel_texts = [a.text() for a in rel_actions]

        self.assertIn("Create 1:1 Relationship", rel_texts)
        self.assertIn("Create 1:n Relationship", rel_texts)
        self.assertIn("Create n:n Relationship", rel_texts)

        conn_actions = connections_menu.actions()
        conn_texts = [a.text() for a in conn_actions if not a.menu()]
        self.assertIn("Create Inheritance Relationship", conn_texts)

    def test_public_action_attributes_exist(self):
        self.assertIsInstance(self.menuBar.actionImportSQL, QAction)
        self.assertIsInstance(self.menuBar.actionExportDiagram, QAction)
        self.assertIsInstance(self.menuBar.actionGenerateSQL, QAction)
        self.assertIsInstance(self.menuBar.actionQuit, QAction)
        self.assertIsInstance(self.menuBar.actionCreateTable, QAction)
        self.assertIsInstance(self.menuBar.actionCreate_1_1_Rel, QAction)
        self.assertIsInstance(self.menuBar.actionCreate_1_n_Rel, QAction)
        self.assertIsInstance(self.menuBar.actionCreate_n_n_Rel, QAction)
        self.assertIsInstance(self.menuBar.actionCreateInheritance, QAction)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)