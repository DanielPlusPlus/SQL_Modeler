import unittest
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

from app.views.MainWindowView import MainWindowView


class TestMainWindowView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PySide6.QtWidgets import QApplication
        import sys
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        self.window = QMainWindow()
        self.view = MainWindowView()
        self.view.setupUi(self.window)

    def testSetupUiSetsObjectNameAndTitle(self):
        self.assertEqual(self.window.objectName(), "MainWindow")
        self.assertEqual(self.window.windowTitle(), "SQL Generator From Diagram")

    def testCentralWidgetAndLayoutsCreated(self):
        central = self.window.centralWidget()
        self.assertIsNotNone(central)
        self.assertIsNotNone(central.layout())
        self.assertTrue(central.layout().inherits("QGridLayout"))

    def testMenuBarAndStatusBarCreated(self):
        self.assertIsNotNone(self.window.menuBar())
        self.assertIsNotNone(self.window.statusBar())

    def testAddCentralWidgetAddsWidgetToHorizontalLayout2(self):
        label = QLabel("Test Label")
        self.view.addCentralWidget(label)
        found = False
        layout = self.view._MainWindowView__horizontalLayout_2
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == label:
                found = True
                break
        self.assertTrue(found)

    def testUpdateStatusBarShowsMessage(self):
        testMessage = "Test Status"
        self.view.updateStatusBar(testMessage)
        status_bar = self.view._MainWindowView__statusBar
        self.assertEqual(status_bar.currentMessage(), testMessage)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
