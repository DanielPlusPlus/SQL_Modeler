import unittest

from app.enums.ConnectionsStatusEnum import ConnectionsStatusEnum


class TestConnectionsStatusEnum(unittest.TestCase):
    def testEnumMembers(self):
        self.assertEqual(ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK.value, 1)
        self.assertEqual(ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK.value, 2)
        self.assertEqual(ConnectionsStatusEnum.NOT_IN_MOTION.value, 3)

    def testEnumNames(self):
        self.assertEqual(ConnectionsStatusEnum(1), ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK)
        self.assertEqual(ConnectionsStatusEnum(2), ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK)
        self.assertEqual(ConnectionsStatusEnum(3), ConnectionsStatusEnum.NOT_IN_MOTION)

    def testEnumIteration(self):
        members = list(ConnectionsStatusEnum)
        self.assertIn(ConnectionsStatusEnum.IN_MOTION_BEFORE_CLICK, members)
        self.assertIn(ConnectionsStatusEnum.IN_MOTION_AFTER_CLICK, members)
        self.assertIn(ConnectionsStatusEnum.NOT_IN_MOTION, members)


if __name__ == "__main__":
    unittest.main()
