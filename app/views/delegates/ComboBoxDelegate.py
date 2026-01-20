from PySide6.QtWidgets import QStyledItemDelegate, QComboBox
from PySide6.QtCore import Qt
from typing import override


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, dataTypes, parent=None):
        super().__init__(parent)
        self.__dataTypes = dataTypes

    @override
    def createEditor(self, parent, option, index):
        comboBox = QComboBox(parent)
        comboBox.addItems(self.__dataTypes)
        return comboBox

    @override
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        valueIndex = editor.findText(value)
        if valueIndex >= 0:
            editor.setCurrentIndex(valueIndex)

    @override
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)
