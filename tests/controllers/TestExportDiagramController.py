import unittest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import QSize

from app.controllers.ExportDiagramController import ExportDiagramController


class TestExportDiagramController(unittest.TestCase):
    def setUp(self):
        self.mockParentWindow = MagicMock()
        self.mockScrollAreaView = MagicMock()
        self.controller = ExportDiagramController(self.mockParentWindow, self.mockScrollAreaView)

    @patch("builtins.print")
    def testExportDiagramToPNGNoWidget(self, mockPrint):
        self.mockScrollAreaView.widget.return_value = None

        self.controller.exportDiagramToPNG()

        mockPrint.assert_called_with("No export widget")

    @patch("app.controllers.ExportDiagramController.QFileDialog.getSaveFileName", return_value=("", ""))
    @patch("app.controllers.ExportDiagramController.QPainter")
    @patch("app.controllers.ExportDiagramController.QPixmap")
    @patch("builtins.print")
    def testExportDiagramToPNGCancelledSave(self, mockPrint, mockQPixmap, mockQPainter, mockGetSaveFileName):
        mockWidget = MagicMock()
        mockWidget.size.return_value = QSize(100, 100)
        self.mockScrollAreaView.widget.return_value = mockWidget

        self.controller.exportDiagramToPNG()

        mockPrint.assert_called_with("Save canceled")
        mockGetSaveFileName.assert_called_once()

    @patch("app.controllers.ExportDiagramController.InfoDialogView")
    @patch("app.controllers.ExportDiagramController.QFileDialog.getSaveFileName", return_value=("output.png", ""))
    @patch("app.controllers.ExportDiagramController.QPainter")
    @patch("app.controllers.ExportDiagramController.QPixmap")
    def testExportDiagramToPNGSuccessfulSave(self, mockQPixmap, mockQPainter, mockGetSaveFileName,
                                             mockInfoDialog):
        mockWidget = MagicMock()
        mockWidget.size.return_value = QSize(100, 100)
        self.mockScrollAreaView.widget.return_value = mockWidget

        mockPixmap = MagicMock()
        mockPixmap.save.return_value = True
        mockQPixmap.return_value = mockPixmap

        self.controller.exportDiagramToPNG()

        mockPixmap.save.assert_called_once_with("output.png", "PNG")
        mockInfoDialog.assert_called_once()
        mockInfoDialog.return_value.displayDialog.assert_called_once()

    @patch("app.controllers.ExportDiagramController.ErrorDialogView")
    @patch("app.controllers.ExportDiagramController.QFileDialog.getSaveFileName", return_value=("output.png", ""))
    @patch("app.controllers.ExportDiagramController.QPainter")
    @patch("app.controllers.ExportDiagramController.QPixmap")
    def testExportDiagramToPNGFailedSave(self, mockQPixmap, mockQPainter, mockGetSaveFileName, mockErrorDialog):
        mockWidget = MagicMock()
        mockWidget.size.return_value = QSize(100, 100)
        self.mockScrollAreaView.widget.return_value = mockWidget

        mockPixmap = MagicMock()
        mockPixmap.save.return_value = False
        mockQPixmap.return_value = mockPixmap

        self.controller.exportDiagramToPNG()

        mockErrorDialog.assert_called_once()
        mockErrorDialog.return_value.displayDialog.assert_called_once()

    @patch("app.controllers.ExportDiagramController.ErrorDialogView")
    @patch("app.controllers.ExportDiagramController.QFileDialog.getSaveFileName", return_value=("output.png", ""))
    @patch("app.controllers.ExportDiagramController.QPainter")
    @patch("app.controllers.ExportDiagramController.QPixmap")
    def testExportDiagramToPNGExceptionDuringSave(self, mockQPixmap, mockQPainter, mockGetSaveFileName,
                                                  mockErrorDialog):
        mockWidget = MagicMock()
        mockWidget.size.return_value = QSize(100, 100)
        self.mockScrollAreaView.widget.return_value = mockWidget

        mockPixmap = MagicMock()
        mockPixmap.save.side_effect = Exception("Unexpected error")
        mockQPixmap.return_value = mockPixmap

        self.controller.exportDiagramToPNG()

        mockErrorDialog.assert_called_once()
        mockErrorDialog.return_value.displayDialog.assert_called_once()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
