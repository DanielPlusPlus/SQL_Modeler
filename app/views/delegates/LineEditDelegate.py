from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QRegularExpressionValidator
from typing import override


class LineEditDelegate(QStyledItemDelegate):
    def __init__(self, regex, maxLength, parent=None):
        super().__init__(parent)
        self.__regex = regex
        self.__maxLength = maxLength

    @override
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QRegularExpressionValidator(self.__regex, editor)
        editor.setValidator(validator)
        editor.setMaxLength(self.__maxLength)
        return editor

    @override
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setText(value)

    @override
    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

