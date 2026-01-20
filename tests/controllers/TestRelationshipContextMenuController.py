import unittest
from unittest.mock import MagicMock

from app.controllers.RelationshipContextMenuController import RelationshipContextMenuController


class TestRelationshipContextMenuController(unittest.TestCase):
    def setUp(self):
        self.mockView = MagicMock()
        self.mockView.actionDeleteRelationship = MagicMock()
        self.mockView.actionDeleteRelationship.triggered.connect = MagicMock()

        self.controller = RelationshipContextMenuController(self.mockView)

    def testInitialState(self):
        self.assertFalse(self.controller.getSelectDeleteRelationshipStatus())

    def testSelectDeleteRelationship(self):
        self.controller._RelationshipContextMenuController__selectDeleteRelationship()
        self.assertTrue(self.controller.getSelectDeleteRelationshipStatus())

    def testUnselectDeleteRelationship(self):
        self.controller._RelationshipContextMenuController__selectDeleteRelationship()
        self.controller.unselectDeleteRelationship()
        self.assertFalse(self.controller.getSelectDeleteRelationshipStatus())

    def testSignalConnections(self):
        self.mockView.actionDeleteRelationship.triggered.connect.assert_called_with(
            self.controller._RelationshipContextMenuController__selectDeleteRelationship
        )


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
