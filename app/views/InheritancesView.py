import math
from PySide6.QtGui import QPainter, QPen, QColor, QPolygonF
from PySide6.QtCore import Qt, QPoint, QPointF

from app.models.InheritanceModel import InheritanceModel


class InheritancesView:
    def __init__(self, InheritanceModel, ParentWindow):
        self.__InheritanceModel = InheritanceModel
        self.__ParentWindow = ParentWindow
        self.drawInheritances()

    def drawInheritances(self):
        painter = QPainter(self.__ParentWindow)
        painter.setRenderHint(QPainter.Antialiasing)

        for inheritance in self.__InheritanceModel.getInheritances():
            line_thickness = inheritance.getLineThickness()
            painter.setPen(QPen(QColor(inheritance.getColor()), line_thickness, Qt.SolidLine))
            child_rect = inheritance.FirstTable.getRectangle()
            parent_rect = inheritance.SecondTable.getRectangle()

            start = self.edgePoint(child_rect, parent_rect)
            arrow_tip = self.edgePoint(parent_rect, child_rect)

            arrow_length, cutoff_distance = self.__getArrowDimensions(line_thickness)
            angle = math.atan2(arrow_tip.y() - start.y(), arrow_tip.x() - start.x())
            line_end = QPointF(
                arrow_tip.x() - cutoff_distance * math.cos(angle),
                arrow_tip.y() - cutoff_distance * math.sin(angle)
            )

            painter.drawLine(start, line_end)
            self.drawInheritanceArrow(painter, arrow_tip, angle, line_thickness)

        painter.end()

    def __getArrowDimensions(self, line_thickness):
        arrow_length = 8 * line_thickness
        cutoff_distance = arrow_length
        return arrow_length, cutoff_distance

    def drawInheritanceArrow(self, painter, tip: QPoint, angle: float, line_thickness: float = 1):
        arrow_length, _ = self.__getArrowDimensions(line_thickness)

        left_angle = angle + math.radians(30)
        right_angle = angle - math.radians(30)

        left = QPointF(
            tip.x() - arrow_length * math.cos(left_angle),
            tip.y() - arrow_length * math.sin(left_angle)
        )
        right = QPointF(
            tip.x() - arrow_length * math.cos(right_angle),
            tip.y() - arrow_length * math.sin(right_angle)
        )

        triangle = QPolygonF([left, tip, right])

        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(triangle)

    def edgePoint(self, start_rect, end_rect):
        center_start = start_rect.center()
        center_end = end_rect.center()

        dx = center_end.x() - center_start.x()
        dy = center_end.y() - center_start.y()

        if dx == 0 and dy == 0:
            return center_start

        if abs(dx) * start_rect.height() > abs(dy) * start_rect.width():
            x = start_rect.right() if dx > 0 else start_rect.left()
            y = center_start.y() + dy * (x - center_start.x()) // dx
        else:
            y = start_rect.bottom() if dy > 0 else start_rect.top()
            x = center_start.x() + dx * (y - center_start.y()) // dy

        return QPoint(x, y)

    def drawInheritanceBeingDrawn(self, FirstTable, cursorPosition, scaleFactor):
        CreatedInheritance = InheritanceModel(FirstTable, None, scaleFactor)
        painter = QPainter(self.__ParentWindow)
        painter.setPen(QPen(QColor(Qt.GlobalColor.black), CreatedInheritance.getLineThickness(), Qt.DashLine))
        painter.setRenderHint(QPainter.Antialiasing)

        first_rect = FirstTable.getRectangle()
        start = self.edgePointToPoint(first_rect, cursorPosition)

        end = cursorPosition if isinstance(cursorPosition, QPoint) else QPoint(cursorPosition.x(), cursorPosition.y())
        painter.drawLine(start, end)
        painter.end()

    def edgePointToPoint(self, start_rect, end_pos):
        center_start = start_rect.center()

        if isinstance(end_pos, QPoint):
            center_end = end_pos
        else:
            center_end = end_pos.center()

        dx = center_end.x() - center_start.x()
        dy = center_end.y() - center_start.y()

        if dx == 0 and dy == 0:
            return center_start

        if abs(dx) * start_rect.height() > abs(dy) * start_rect.width():
            x = start_rect.right() if dx > 0 else start_rect.left()
            y = center_start.y() + dy * (x - center_start.x()) // dx
        else:
            y = start_rect.bottom() if dy > 0 else start_rect.top()
            x = center_start.x() + dx * (y - center_start.y()) // dy

        return QPoint(x, y)