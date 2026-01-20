import unittest

from app.enums.TableContextMenuEnum import TableContextMenuEnum


class TestTableContextMenuEnum(unittest.TestCase):
    def testEnumValues(self):
        self.assertEqual(TableContextMenuEnum.COLLAPSE.value, 1)
        self.assertEqual(TableContextMenuEnum.EDIT.value, 2)
        self.assertEqual(TableContextMenuEnum.DELETE.value, 3)
        self.assertEqual(TableContextMenuEnum.NONE.value, 4)

    def testEnumMembersFromValue(self):
        self.assertIs(TableContextMenuEnum(1), TableContextMenuEnum.COLLAPSE)
        self.assertIs(TableContextMenuEnum(2), TableContextMenuEnum.EDIT)
        self.assertIs(TableContextMenuEnum(3), TableContextMenuEnum.DELETE)
        self.assertIs(TableContextMenuEnum(4), TableContextMenuEnum.NONE)

    def testEnumIteration(self):
        members = list(TableContextMenuEnum)
        self.assertIn(TableContextMenuEnum.COLLAPSE, members)
        self.assertIn(TableContextMenuEnum.EDIT, members)
        self.assertIn(TableContextMenuEnum.DELETE, members)
        self.assertIn(TableContextMenuEnum.NONE, members)


if __name__ == "__main__":
    unittest.main()
