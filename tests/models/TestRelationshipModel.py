import unittest
from unittest.mock import MagicMock

from app.models.RelationshipModel import RelationshipModel
from app.models.ConnectionModel import ConnectionModel


class TestRelationshipModel(unittest.TestCase):
    def setUp(self):
        self.firstTable = MagicMock()
        self.secondTable = MagicMock()
        self.firstColumn = "id"
        self.secondColumn = "user_id"
        self.relType = "1:n"
        self.relationship = RelationshipModel(
            self.firstTable,
            self.secondTable,
            self.firstColumn,
            self.secondColumn,
            self.relType
        )

    def testInstanceIsConnectionModel(self):
        self.assertIsInstance(self.relationship, ConnectionModel)

    def testGetFirstSelectedColumnName(self):
        self.assertEqual(self.relationship.getFirstSelectedColumnName(), self.firstColumn)

    def testGetSecondSelectedColumnName(self):
        self.assertEqual(self.relationship.getSecondSelectedColumnName(), self.secondColumn)

    def testGetRelationshipType(self):
        self.assertEqual(self.relationship.getRelationshipType(), self.relType)

    def testGetFirstAndSecondTable(self):
        self.assertEqual(self.relationship.getFirstTable(), self.firstTable)
        self.assertEqual(self.relationship.getSecondTable(), self.secondTable)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
