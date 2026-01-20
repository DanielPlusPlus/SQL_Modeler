import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app.MainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("app\\icons\\icon.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
