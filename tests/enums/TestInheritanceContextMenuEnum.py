import unittest

from app.enums.InheritanceContextMenuEnum import InheritanceContextMenuEnum


class TestInheritanceContextMenuEnum(unittest.TestCase):
    def testEnumValues(self):
        self.assertEqual(InheritanceContextMenuEnum.DELETE.value, 1)
        self.assertEqual(InheritanceContextMenuEnum.NONE.value, 2)

    def testEnumMembersFromValue(self):
        self.assertIs(InheritanceContextMenuEnum(1), InheritanceContextMenuEnum.DELETE)
        self.assertIs(InheritanceContextMenuEnum(2), InheritanceContextMenuEnum.NONE)

    def testEnumIteration(self):
        members = list(InheritanceContextMenuEnum)
        self.assertIn(InheritanceContextMenuEnum.DELETE, members)
        self.assertIn(InheritanceContextMenuEnum.NONE, members)


if __name__ == "__main__":
    unittest.main()
