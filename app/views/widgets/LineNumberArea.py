from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget
from typing import override


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.__code_editor = editor

    @override
    def sizeHint(self):
        return QSize(self.__code_editor.line_number_area_width(), 0)

    @override
    def paintEvent(self, event):
        self.__code_editor.line_number_area_paint_event(event)