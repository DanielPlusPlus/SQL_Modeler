from PySide6.QtWidgets import QColorDialog, QWidget, QPushButton, QGridLayout, QHBoxLayout
from PySide6.QtGui import QColor


class ColorChangeDialogView(QColorDialog):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)
        self.__customColors = [
            "#FFFF99",
            "#99FF99",
            "#99CCFF",
            "#FF9999",
            "#FFCC99",
            "#FF99CC",
            "#99FFCC",
            "#CCCCCC"
        ]

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"ColorChangeDialog")
        self.resize(600, 400)
        self.setWindowTitle(u"Change Color")

        for color in self.__customColors:
            self.setCustomColor(self.__customColors.index(color), QColor(color))
        self.setOption(QColorDialog.ShowAlphaChannel, False)
        self.setOption(QColorDialog.DontUseNativeDialog, True)
        self.setOption(QColorDialog.NoButtons, True)

        self.__gridLayout = QGridLayout(self)
        self.__horizontalLayout = QHBoxLayout()
        self.__horizontalLayout_2 = QHBoxLayout()
        self.__horizontalLayout_3 = QHBoxLayout()
        self.__horizontalLayout_4 = QHBoxLayout()
        self.__pleceholderWidget = QWidget(self)
        self.cancelButton = QPushButton(u"Cancel", self)
        self.okButton = QPushButton(u"OK", self)
        self.__horizontalLayout_2.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_3.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_4.addWidget(self.cancelButton)
        self.__horizontalLayout_4.addWidget(self.okButton)
        self.__horizontalLayout.addLayout(self.__horizontalLayout_2)
        self.__horizontalLayout.addLayout(self.__horizontalLayout_3)
        self.__horizontalLayout.addLayout(self.__horizontalLayout_4)
        self.__horizontalLayout.setStretch(0, 1)
        self.__horizontalLayout.setStretch(1, 1)
        self.__horizontalLayout.setStretch(2, 1)
        self.__gridLayout.addLayout(self.__horizontalLayout, 0, 0, 1, 1)

        self.__gridLayout.setRowStretch(0, 1)
        self.__gridLayout.setRowStretch(1, 1)

        originalLayout = self.layout()
        originalLayout.addLayout(self.__gridLayout)
        self.setLayout(originalLayout)

    def displayDialog(self):
        result = self.exec()
        return result
