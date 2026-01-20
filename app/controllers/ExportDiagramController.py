from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QPoint

from app.views.InfoDialogView import InfoDialogView
from app.views.ErrorDialogView import ErrorDialogView


class ExportDiagramController:
    def __init__(self, ParentWindow, ScrollAreaView):
        self.__ParentWindow = ParentWindow
        self.__ScrollAreaView = ScrollAreaView

    def exportDiagramToPNG(self):
        widget = self.__ScrollAreaView.widget()
        if widget is None:
            print("No export widget")
            return

        pixmap = QPixmap(widget.size())
        pixmap.fill()

        painter = QPainter(pixmap)
        widget.render(painter, QPoint(0, 0))
        painter.end()

        filePath, _ = QFileDialog.getSaveFileName(
            self.__ParentWindow,
            "Save diagram as PNG",
            "",
            "PNG files (*.png)"
        )
        if not filePath:
            print("Save canceled")
            return

        try:
            if pixmap.save(filePath, "PNG"):
                dialogTitle = "EXPORT"
                dialogText = "Diagram has been successfully saved to a file"
                InfoDialog = InfoDialogView(self.__ParentWindow, dialogTitle, dialogText)
                InfoDialog.displayDialog()
            else:
                dialogTitle = "ERROR"
                dialogText = f"Failed to save file"
                ErrorDialog = ErrorDialogView(self.__ParentWindow, dialogTitle, dialogText)
                ErrorDialog.displayDialog()
        except Exception as e:
            dialogTitle = "ERROR"
            dialogText = f"Failed to save file:\n{str(e)}"
            ErrorDialog = ErrorDialogView(self.__ParentWindow, dialogTitle, dialogText)
            ErrorDialog.displayDialog()
