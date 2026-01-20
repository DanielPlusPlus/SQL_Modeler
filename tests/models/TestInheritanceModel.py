import unittest
from unittest.mock import MagicMock

from app.models.InheritanceModel import InheritanceModel
from app.models.ConnectionModel import ConnectionModel


class DummyTable:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def getRectangle(self):
        class Rect:
            def center(self_inner):
                class Point:
                    def x(self_point): return self._x

                    def y(self_point): return self._y

                    def __sub__(self_point, other):
                        return self_point

                    def manhattanLength(self_point):
                        return abs(self._x) + abs(self._y)

                return Point()

        return Rect()


class TestInheritanceModel(unittest.TestCase):
    def setUp(self):
        self.firstTable = MagicMock()
        self.secondTable = MagicMock()
        self.inheritance = InheritanceModel(self.firstTable, self.secondTable)

    def testInstanceIsConnectionModel(self):
        self.assertIsInstance(self.inheritance, ConnectionModel)

    def testFirstAndSecondTableAssigned(self):
        self.assertEqual(self.inheritance.getFirstTable(), self.firstTable)
        self.assertEqual(self.inheritance.getSecondTable(), self.secondTable)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
