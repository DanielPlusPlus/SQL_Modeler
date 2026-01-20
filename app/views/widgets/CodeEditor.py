from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QColor, QPainter, QTextFormat, QFont
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit
from typing import override

from app.views.widgets.LineNumberArea import LineNumberArea


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont("Courier", 10)
        self.setFont(font)

        self.__line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.__update_line_number_area_width)
        self.updateRequest.connect(self.__update_line_number_area)
        self.cursorPositionChanged.connect(self.__highlight_current_line)

        self.__update_line_number_area_width(0)
        self.__highlight_current_line()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def __update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def __update_line_number_area(self, rect, dy):
        if dy:
            self.__line_number_area.scroll(0, dy)
        else:
            self.__line_number_area.update(0, rect.y(), self.__line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.__update_line_number_area_width(0)

    @override
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.__line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.__line_number_area)
        painter.fillRect(event.rect(), QColor(240, 240, 240))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.gray)
                painter.drawText(0, top, self.__line_number_area.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def __highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(232, 242, 254)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)
