import math
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint, QPointF

from app.enums.RelationshipsEnum import RelationshipsEnum


class RelationshipsView:
    def __init__(self, RelationshipsModel, ParentWindow):
        self.RelationshipsModel = RelationshipsModel
        self.ParentWindow = ParentWindow
        self.drawRelationships()

    def drawRelationships(self):
        painter = QPainter(self.ParentWindow)
        painter.setPen(QPen(QColor(Qt.GlobalColor.black), 2, Qt.PenStyle.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing)

        for rel in self.RelationshipsModel.getRelationships():
            first_rect = rel.FirstTable.getRectangle()
            second_rect = rel.SecondTable.getRectangle()

            start = self.edgePoint(first_rect, second_rect)
            end = self.edgePoint(second_rect, first_rect)

            painter.drawLine(start, end)

            self.drawRelationshipSymbol(painter, start, end, rel.getRelationshipType())

        painter.end()

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

    def drawRelationshipSymbol(self, painter, start: QPoint, end: QPoint, rel_type: str):
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())

        def offset_point(point: QPoint, angle: float, distance: float) -> QPointF:
            return QPointF(
                point.x() - distance * math.cos(angle),
                point.y() - distance * math.sin(angle)
            )

        def draw_bar(point, offset=0):
            size = 6
            perp = angle + math.pi / 2
            dx = size * math.cos(perp)
            dy = size * math.sin(perp)
            ox = offset * math.cos(angle)
            oy = offset * math.sin(angle)
            x = point.x() + ox
            y = point.y() + oy
            p1 = QPointF(x - dx, y - dy)
            p2 = QPointF(x + dx, y + dy)
            painter.drawLine(p1, p2)

        def draw_crows_foot(point, flip=False):
            spread = 0.4
            length = 12
            base_angle = angle + math.pi if flip else angle
            for a in [-spread, 0, spread]:
                dx = length * math.cos(base_angle + a)
                dy = length * math.sin(base_angle + a)
                painter.drawLine(point, QPointF(point.x() + dx, point.y() + dy))

        offset_distance = 12

        if rel_type is RelationshipsEnum.REL_1_1:
            draw_bar(offset_point(start, angle, -offset_distance), offset=12)
            draw_bar(offset_point(end, angle, offset_distance), offset=-12)
        elif rel_type is RelationshipsEnum.REL_1_n:
            draw_bar(offset_point(start, angle, -offset_distance), offset=12)
            draw_crows_foot(offset_point(end, angle, offset_distance))
        elif rel_type is RelationshipsEnum.REL_n_n:
            draw_crows_foot(offset_point(start, angle, -offset_distance), flip=True)
            draw_crows_foot(offset_point(end, angle, offset_distance))

    def drawRelationshipBeingDrawn(self, FirstTable, cursorPosition):
        painter = QPainter(self.ParentWindow)
        painter.setPen(QPen(QColor(Qt.GlobalColor.black), 2, Qt.PenStyle.DashLine))
        painter.setRenderHint(QPainter.Antialiasing)

        first_rect = FirstTable.getRectangle()
        start = self.edgePoint2(first_rect, cursorPosition)

        end = cursorPosition if isinstance(cursorPosition, QPoint) else QPoint(cursorPosition.x(), cursorPosition.y())

        painter.drawLine(start, end)
        painter.end()

    def edgePoint2(self, start_rect, end_pos):
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
