import unittest
from unittest.mock import MagicMock
from PySide6.QtCore import QPoint

from app.models.RelationshipsModel import RelationshipsModel
from app.models.RelationshipModel import RelationshipModel
from app.enums.RelationshipsEnum import RelationshipsEnum


class DummyTable:
    pass


class TestRelationshipsModel(unittest.TestCase):
    def setUp(self):
        self.model = RelationshipsModel()
        self.table1 = DummyTable()
        self.table2 = DummyTable()
        self.table3 = DummyTable()

    def test_add_1_1_relationship(self):
        self.model.add_1_1_Relationship(self.table1, self.table2, "id1", "id2")

        rels = self.model.getRelationships()
        self.assertEqual(len(rels), 1)
        rel = rels[0]

        self.assertIsInstance(rel, RelationshipModel)
        self.assertIs(rel.getFirstTable(), self.table1)
        self.assertIs(rel.getSecondTable(), self.table2)
        self.assertEqual(rel.getFirstSelectedColumnName(), "id1")
        self.assertEqual(rel.getSecondSelectedColumnName(), "id2")
        self.assertEqual(rel.getRelationshipType(), RelationshipsEnum.REL_1_1)

    def test_add_1_n_relationship(self):
        self.model.add_1_n_Relationship(self.table1, self.table2, "id1", "id2")

        rels = self.model.getRelationships()
        self.assertEqual(len(rels), 1)
        rel = rels[0]

        self.assertEqual(rel.getRelationshipType(), RelationshipsEnum.REL_1_n)

    def test_add_n_n_relationship(self):
        self.model.add_n_n_Relationship(self.table1, self.table2, "id1", "id2")

        rels = self.model.getRelationships()
        self.assertEqual(len(rels), 1)
        rel = rels[0]

        self.assertEqual(rel.getRelationshipType(), RelationshipsEnum.REL_n_n)

    def test_addRelationship_accepts_only_relationshipmodel(self):
        rel = RelationshipModel(self.table1, self.table2, "id1", "id2", RelationshipsEnum.REL_1_1)
        self.model.addRelationship(rel)
        self.assertIn(rel, self.model.getRelationships())

        with self.assertRaises(TypeError):
            self.model.addRelationship("not_a_relationship")

    def test_clear_relationships(self):
        self.model.add_1_1_Relationship(self.table1, self.table2, "id1", "id2")
        self.model.add_1_n_Relationship(self.table1, self.table3, "id1", "id3")
        self.assertGreater(len(self.model.getRelationships()), 0)

        self.model.clearRelationships()
        self.assertEqual(len(self.model.getRelationships()), 0)

    def test_delete_selected_relationship(self):
        rel1 = RelationshipModel(self.table1, self.table2, "id1", "id2", RelationshipsEnum.REL_1_1)
        rel2 = RelationshipModel(self.table2, self.table3, "id2", "id3", RelationshipsEnum.REL_1_n)
        self.model.addRelationship(rel1)
        self.model.addRelationship(rel2)

        self.model.deleteSelectedRelationship(rel1)

        rels = self.model.getRelationships()
        self.assertEqual(len(rels), 1)
        self.assertIs(rels[0], rel2)

    def test_delete_relationship_by_table(self):
        rel1 = RelationshipModel(self.table1, self.table2, "id1", "id2", RelationshipsEnum.REL_1_1)
        rel2 = RelationshipModel(self.table2, self.table3, "id2", "id3", RelationshipsEnum.REL_1_n)
        rel3 = RelationshipModel(self.table1, self.table3, "id1", "id3", RelationshipsEnum.REL_n_n)

        self.model.addRelationship(rel1)
        self.model.addRelationship(rel2)
        self.model.addRelationship(rel3)

        self.model.deleteRelationshipByTable(self.table2)

        rels = self.model.getRelationships()
        self.assertEqual(len(rels), 1)
        self.assertIs(rels[0], rel3)

    def test_get_relationship_from_position_returns_matching(self):
        rel = RelationshipModel(self.table1, self.table2, "id1", "id2", RelationshipsEnum.REL_1_1)
        rel.contains = MagicMock(return_value=True)
        self.model.addRelationship(rel)

        pos = QPoint(10, 10)
        found = self.model.getRelationshipFromPosition(pos)
        self.assertIs(found, rel)
        rel.contains.assert_called_once()
        called_arg = rel.contains.call_args[0][0]
        self.assertIsInstance(called_arg, QPoint)
        self.assertEqual(called_arg.x(), pos.x())
        self.assertEqual(called_arg.y(), pos.y())

    def test_get_relationship_from_position_returns_none_if_no_match(self):
        rel = RelationshipModel(self.table1, self.table2, "id1", "id2", RelationshipsEnum.REL_1_1)
        rel.contains = MagicMock(return_value=False)
        self.model.addRelationship(rel)

        pos = QPoint(5, 5)
        found = self.model.getRelationshipFromPosition(pos)
        self.assertIsNone(found)
        rel.contains.assert_called_once()


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
