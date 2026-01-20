import unittest
from unittest.mock import MagicMock
from PySide6.QtCore import QPoint

from app.controllers.MainWindowController import MainWindowController


class TestMainWindowController(unittest.TestCase):
    def setUp(self):
        self.mockMainWindow = MagicMock()
        self.mockView = MagicMock()
        self.controller = MainWindowController(self.mockMainWindow, self.mockView)

    def testUpdateStatusBarInViewCallsUpdateStatusBarWithCorrectMessage(self):
        position = QPoint(123, 456)

        self.controller.updateStatusBarInView(position)

        expectedMessage = "Current mouse position: x - 123, y - 456"
        self.mockView.updateStatusBar.assert_called_once_with(expectedMessage)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
