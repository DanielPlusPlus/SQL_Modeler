import sys
import unittest

from PySide6.QtWidgets import QApplication, QLineEdit
from PySide6.QtCore import Qt, QRegularExpression, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem

from app.views.delegates.LineEditDelegate import LineEditDelegate

app = QApplication.instance() or QApplication(sys.argv)


class TestLineEditDelegate(unittest.TestCase):
    def setUp(self):
        self.regex = QRegularExpression(r"[A-Za-z0-9_]+")
        self.maxLength = 10
        self.delegate = LineEditDelegate(self.regex, self.maxLength)

        self.model = QStandardItemModel(1, 1)
        item = QStandardItem("Initial")
        self.model.setItem(0, 0, item)
        self.index: QModelIndex = self.model.index(0, 0)

    def test_create_editor_type_and_properties(self):
        parent = None
        editor = self.delegate.createEditor(parent, None, self.index)

        self.assertIsInstance(editor, QLineEdit)
        self.assertIsNotNone(editor.validator())
        self.assertEqual(editor.maxLength(), self.maxLength)

    def test_create_editor_validator_uses_given_regex(self):
        editor = self.delegate.createEditor(None, None, self.index)
        validator = editor.validator()
        self.assertIsNotNone(validator)
        self.assertEqual(validator.regularExpression().pattern(), self.regex.pattern())

    def test_set_editor_data_sets_text_from_model(self):
        editor = QLineEdit()
        self.model.setData(self.index, "Hello", Qt.EditRole)

        self.delegate.setEditorData(editor, self.index)

        self.assertEqual(editor.text(), "Hello")

    def test_set_model_data_writes_back_to_model(self):
        editor = QLineEdit()
        editor.setText("NewValue")

        self.delegate.setModelData(editor, self.model, self.index)

        self.assertEqual(self.model.data(self.index, Qt.EditRole), "NewValue")


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)