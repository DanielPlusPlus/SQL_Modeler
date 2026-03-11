import math

from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint, QPointF

from app.models.RelationshipModel import RelationshipModel
from app.enums.RelationshipsEnum import RelationshipsEnum


class RelationshipsView:
    def __init__(self, RelationshipsModel, ParentWindow):
        self.RelationshipsModel = RelationshipsModel
        self.ParentWindow = ParentWindow
        self.drawRelationships()

    def __getTableRect(self, table):
        if table.getTableCollapseStatus():
            return table.getTitleRectangle()
        return table.getRectangle()

    def drawRelationships(self):
        painter = QPainter(self.ParentWindow)
        painter.setRenderHint(QPainter.Antialiasing)

        for rel in self.RelationshipsModel.getRelationships():
            line_thickness = rel.getLineThickness()
            painter.setPen(QPen(QColor(rel.getColor()), line_thickness, Qt.PenStyle.SolidLine))
            first_rect = self.__getTableRect(rel.FirstTable)
            second_rect = self.__getTableRect(rel.SecondTable)

            start = self.edgePoint(first_rect, second_rect)
            end = self.edgePoint(second_rect, first_rect)

            painter.drawLine(start, end)

            self.drawRelationshipSymbol(painter, start, end, rel.getRelationshipType(), line_thickness)

        painter.end()

    def __getSymbolDimensions(self, line_thickness):
        bar_size = 4 * line_thickness
        crows_foot_length = 8 * line_thickness
        offset_distance = 8 * line_thickness
        return bar_size, crows_foot_length, offset_distance

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

    def drawRelationshipSymbol(self, painter, start: QPoint, end: QPoint, rel_type: str, line_thickness: float = 1):
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        bar_size, crows_foot_length, offset_distance = self.__getSymbolDimensions(line_thickness)

        def offset_point(point: QPoint, angle: float, distance: float) -> QPointF:
            return QPointF(
                point.x() - distance * math.cos(angle),
                point.y() - distance * math.sin(angle)
            )

        def draw_bar(point, offset=0):
            perp = angle + math.pi / 2
            dx = bar_size * math.cos(perp)
            dy = bar_size * math.sin(perp)
            ox = offset * math.cos(angle)
            oy = offset * math.sin(angle)
            x = point.x() + ox
            y = point.y() + oy
            p1 = QPointF(x - dx, y - dy)
            p2 = QPointF(x + dx, y + dy)
            painter.drawLine(p1, p2)

        def draw_crows_foot(point, flip=False):
            spread = 0.4
            base_angle = angle + math.pi if flip else angle
            for a in [-spread, 0, spread]:
                dx = crows_foot_length * math.cos(base_angle + a)
                dy = crows_foot_length * math.sin(base_angle + a)
                painter.drawLine(point, QPointF(point.x() + dx, point.y() + dy))

        if rel_type is RelationshipsEnum.REL_1_1:
            draw_bar(offset_point(start, angle, -offset_distance), offset=offset_distance)
            draw_bar(offset_point(end, angle, offset_distance), offset=-offset_distance)
        elif rel_type is RelationshipsEnum.REL_1_n:
            draw_bar(offset_point(start, angle, -offset_distance), offset=offset_distance)
            draw_crows_foot(offset_point(end, angle, offset_distance))
        elif rel_type is RelationshipsEnum.REL_n_n:
            draw_crows_foot(offset_point(start, angle, -offset_distance), flip=True)
            draw_crows_foot(offset_point(end, angle, offset_distance))

    def drawRelationshipBeingDrawn(self, FirstTable, cursorPosition, scaleFactor):
        CreatedRelationship = RelationshipModel(FirstTable, None, None, None, None, scaleFactor)
        painter = QPainter(self.ParentWindow)
        painter.setPen(QPen(QColor(CreatedRelationship.getColor()), CreatedRelationship.getLineThickness(),
                            Qt.PenStyle.DashLine))
        painter.setRenderHint(QPainter.Antialiasing)

        first_rect = self.__getTableRect(FirstTable)
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