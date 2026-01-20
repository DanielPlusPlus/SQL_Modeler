import unittest

from app.enums.RelationshipsEnum import RelationshipsEnum


class TestRelationshipsEnum(unittest.TestCase):
    def testEnumValues(self):
        self.assertEqual(RelationshipsEnum.REL_1_1.value, 1)
        self.assertEqual(RelationshipsEnum.REL_1_n.value, 2)
        self.assertEqual(RelationshipsEnum.REL_n_n.value, 3)

    def testEnumMembersFromValue(self):
        self.assertIs(RelationshipsEnum(1), RelationshipsEnum.REL_1_1)
        self.assertIs(RelationshipsEnum(2), RelationshipsEnum.REL_1_n)
        self.assertIs(RelationshipsEnum(3), RelationshipsEnum.REL_n_n)

    def testEnumIteration(self):
        members = list(RelationshipsEnum)
        self.assertIn(RelationshipsEnum.REL_1_1, members)
        self.assertIn(RelationshipsEnum.REL_1_n, members)
        self.assertIn(RelationshipsEnum.REL_n_n, members)


if __name__ == "__main__":
    unittest.main()
