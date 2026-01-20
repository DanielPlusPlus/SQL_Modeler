import unittest
import sys
from PySide6.QtWidgets import QApplication, QMainWindow


class TestMainWindow(unittest.TestCase):
    def testQApplicationCanBeCreated(self):
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            self.assertIsNotNone(app)

            window = QMainWindow()
            self.assertIsNotNone(window)
        except Exception as e:
            self.fail(f"Creating QApplication or QMainWindow failed: {e}")


if __name__ == '__main__':
    unittest.main()
