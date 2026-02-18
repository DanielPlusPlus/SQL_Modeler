from app.views.ConfirmationDialogView import ConfirmationDialogView


class MainWindowController:
    def __init__(self, MainWindow, MainWindowView):
        self.__MainWindow = MainWindow
        self.__MainWindowView = MainWindowView
        self.__allowCloseWithoutConfirmation = True

    def updateStatusBarInView(self, position):
        message = "Current mouse position: x - " + str(position.x()) + ", y - " + str(position.y())
        self.__MainWindowView.updateStatusBar(message)

    def setWidgetToCentralWidget(self, ScrollAreaView):
        self.__MainWindowView.setWidgetToCentralWidget(ScrollAreaView)

    def selectCloseWithoutConfirmation(self):
        self.__allowCloseWithoutConfirmation = True

    def unselectCloseWithoutConfirmation(self):
        self.__allowCloseWithoutConfirmation = False

    def __getCloseWithoutConfirmationStatus(self):
        return self.__allowCloseWithoutConfirmation

    def closeWindow(self):
        if self.__getCloseWithoutConfirmationStatus():
            self.__MainWindow.close()
        else:
            dialogTitle = "WARNING"
            dialogText = "Are you sure about exiting without saving?"
            ConfirmationDialog = ConfirmationDialogView(self.__MainWindow, dialogTitle, dialogText)
            if ConfirmationDialog.displayDialog():
                self.__MainWindow.close()
