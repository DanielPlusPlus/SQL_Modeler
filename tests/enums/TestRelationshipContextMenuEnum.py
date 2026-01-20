import unittest

from app.enums.RelationshipContextMenuEnum import RelationshipContextMenuEnum


class TestRelationshipContextMenuEnum(unittest.TestCase):
    def testEnumValues(self):
        self.assertEqual(RelationshipContextMenuEnum.DELETE.value, 1)
        self.assertEqual(RelationshipContextMenuEnum.NONE.value, 2)

    def testEnumMembersFromValue(self):
        self.assertIs(RelationshipContextMenuEnum(1), RelationshipContextMenuEnum.DELETE)
        self.assertIs(RelationshipContextMenuEnum(2), RelationshipContextMenuEnum.NONE)

    def testEnumIteration(self):
        members = list(RelationshipContextMenuEnum)
        self.assertIn(RelationshipContextMenuEnum.DELETE, members)
        self.assertIn(RelationshipContextMenuEnum.NONE, members)


if __name__ == "__main__":
    unittest.main()
