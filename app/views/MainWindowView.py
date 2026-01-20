from PySide6.QtCore import QCoreApplication, QMetaObject, QRect
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QMenuBar, QStatusBar, QWidget


class MainWindowView:
    def setupUi(self, parentWindow):
        if not parentWindow.objectName():
            parentWindow.setObjectName(u"MainWindow")
        parentWindow.resize(800, 600)
        self.__centralwidget = QWidget(parentWindow)
        self.__gridLayout = QGridLayout(self.__centralwidget)
        self.__horizontalLayout_1 = QHBoxLayout()

        self.__gridLayout.addLayout(self.__horizontalLayout_1, 0, 0, 1, 1)

        self.__horizontalLayout_2 = QHBoxLayout()

        self.__gridLayout.addLayout(self.__horizontalLayout_2, 1, 0, 1, 1)

        parentWindow.setCentralWidget(self.__centralwidget)
        self.__menuBar = QMenuBar(parentWindow)
        self.__menuBar.setGeometry(QRect(0, 0, 800, 22))
        parentWindow.setMenuBar(self.__menuBar)
        self.__statusBar = QStatusBar(parentWindow)
        parentWindow.setStatusBar(self.__statusBar)
        self.__retranslateUi(parentWindow)

    def __retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SQL Generator From Diagram", None))

    def addCentralWidget(self, widget):
        self.__horizontalLayout_2.addWidget(widget)

    def updateStatusBar(self, message):
        self.__statusBar.showMessage(message)
