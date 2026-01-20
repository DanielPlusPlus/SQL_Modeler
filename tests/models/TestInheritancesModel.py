import unittest
from unittest.mock import MagicMock
from PySide6.QtCore import QPoint

from app.models.InheritancesModel import InheritancesModel
from app.models.InheritanceModel import InheritanceModel


class TestInheritancesModel(unittest.TestCase):
    def setUp(self):
        self.model = InheritancesModel()
        self.table1 = MagicMock()
        self.table2 = MagicMock()
        self.table3 = MagicMock()

    def testAddAndGetInheritances(self):
        self.model.addInheritance(self.table1, self.table2)
        inheritances = self.model.getInheritances()
        self.assertEqual(len(inheritances), 1)
        self.assertIsInstance(inheritances[0], InheritanceModel)
        self.assertEqual(inheritances[0].getFirstTable(), self.table1)
        self.assertEqual(inheritances[0].getSecondTable(), self.table2)

    def testClearInheritances(self):
        self.model.addInheritance(self.table1, self.table2)
        self.model.clearInheritances()
        self.assertEqual(len(self.model.getInheritances()), 0)

    def testDeleteSelectedInheritance(self):
        self.model.addInheritance(self.table1, self.table2)
        inheritance = self.model.getInheritances()[0]
        self.model.deleteSelectedInheritance(inheritance)
        self.assertEqual(len(self.model.getInheritances()), 0)

    def testDeleteInheritanceByTable(self):
        self.model.addInheritance(self.table1, self.table2)
        self.model.addInheritance(self.table2, self.table3)
        self.model.deleteInheritanceByTable(self.table2)
        inheritances = self.model.getInheritances()
        self.assertEqual(len(inheritances), 0)

        self.model.addInheritance(self.table1, self.table2)
        self.model.addInheritance(self.table2, self.table3)
        self.model.deleteInheritanceByTable(self.table1)
        inheritances = self.model.getInheritances()
        self.assertEqual(len(inheritances), 1)
        self.assertNotIn(self.table1, (inheritances[0].getFirstTable(), inheritances[0].getSecondTable()))

    def testGetInheritanceFromPosition(self):
        inheritanceMock = MagicMock()
        inheritanceMock.contains.return_value = False
        self.model._InheritancesModel__inheritances.append(inheritanceMock)

        pos = QPoint(10, 20)
        self.assertIsNone(self.model.getInheritanceFromPosition(pos))

        inheritanceMock.contains.return_value = True
        found = self.model.getInheritanceFromPosition(pos)
        self.assertIs(found, inheritanceMock)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)