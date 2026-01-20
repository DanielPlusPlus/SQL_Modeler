from PySide6.QtWidgets import QStyledItemDelegate, QSpinBox
from typing import override


class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, minValue, maxValue, parent=None):
        super().__init__(parent)
        self.__minValue = minValue
        self.__maxValue = maxValue

    @override
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setRange(self.__minValue, self.__maxValue)
        editor.setSpecialValueText("DEFAULT")
        return editor
