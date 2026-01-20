import unittest


class PointMock:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    def __sub__(self, other):
        return PointMock(self._x - other._x, self._y - other._y)

    def manhattanLength(self):
        return abs(self._x) + abs(self._y)


class RectangleMock:
    def __init__(self, centerPoint):
        self._center = centerPoint

    def center(self):
        return self._center


class TableMock:
    def __init__(self, centerPoint):
        self._rectangle = RectangleMock(centerPoint)

    def getRectangle(self):
        return self._rectangle


from app.models.ConnectionModel import ConnectionModel


class TestConnectionModel(unittest.TestCase):
    def setUp(self):
        self.firstTable = TableMock(PointMock(0, 0))
        self.secondTable = TableMock(PointMock(10, 0))
        self.connection = ConnectionModel(self.firstTable, self.secondTable)

    def testGetFirstTable(self):
        self.assertEqual(self.connection.getFirstTable(), self.firstTable)

    def testGetSecondTable(self):
        self.assertEqual(self.connection.getSecondTable(), self.secondTable)

    def testContainsPointOnLine(self):
        point = PointMock(5, 0)
        self.assertTrue(self.connection.contains(point))

    def testContainsPointNearLineWithinThreshold(self):
        point = PointMock(5, 3)
        self.assertTrue(self.connection.contains(point))

    def testContainsPointFarFromLine(self):
        point = PointMock(5, 10)
        self.assertFalse(self.connection.contains(point))

    def testContainsPointOnStartPoint(self):
        point = PointMock(0, 0)
        self.assertTrue(self.connection.contains(point))

    def testContainsPointOnEndPoint(self):
        point = PointMock(10, 0)
        self.assertTrue(self.connection.contains(point))

    def testContainsSinglePointConnection(self):
        firstTable = TableMock(PointMock(1, 1))
        secondTable = TableMock(PointMock(1, 1))
        connection = ConnectionModel(firstTable, secondTable)
        point = PointMock(1, 1)
        self.assertTrue(connection.contains(point))
        pointFar = PointMock(10, 10)
        self.assertFalse(connection.contains(pointFar))


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
