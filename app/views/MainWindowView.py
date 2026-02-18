from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QStatusBar, QWidget


class MainWindowView:
    def setupUi(self, parentWindow):
        if not parentWindow.objectName():
            parentWindow.setObjectName(u"MainWindow")
        parentWindow.resize(800, 600)
        self.__centralWidget = QWidget(parentWindow)
        self.__gridLayout = QGridLayout(self.__centralWidget)
        self.__horizontalLayout = QHBoxLayout()
        self.__gridLayout.addLayout(self.__horizontalLayout, 0, 0, 1, 1)
        parentWindow.setCentralWidget(self.__centralWidget)
        self.__statusBar = QStatusBar(parentWindow)
        parentWindow.setStatusBar(self.__statusBar)
        self.__retranslateUi(parentWindow)

    def __retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SQL Generator From Diagram", None))

    def setWidgetToCentralWidget(self, widget):
        self.__horizontalLayout.addWidget(widget)

    def updateStatusBar(self, message):
        self.__statusBar.showMessage(message)
