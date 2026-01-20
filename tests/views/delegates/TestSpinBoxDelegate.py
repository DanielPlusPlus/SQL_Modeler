import sys
import unittest

from PySide6.QtWidgets import QApplication, QSpinBox
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem

from app.views.delegates.SpinBoxDelegate import SpinBoxDelegate

app = QApplication.instance() or QApplication(sys.argv)


class TestSpinBoxDelegate(unittest.TestCase):
    def setUp(self):
        self.minValue = 1
        self.maxValue = 99
        self.delegate = SpinBoxDelegate(self.minValue, self.maxValue)

        self.model = QStandardItemModel(1, 1)
        item = QStandardItem()
        item.setData(10)
        self.model.setItem(0, 0, item)
        self.index: QModelIndex = self.model.index(0, 0)

    def test_create_editor_type_and_range(self):
        parent = None
        editor = self.delegate.createEditor(parent, None, self.index)

        self.assertIsInstance(editor, QSpinBox)
        self.assertEqual(editor.minimum(), self.minValue)
        self.assertEqual(editor.maximum(), self.maxValue)

    def test_create_editor_special_value_text(self):
        editor = self.delegate.createEditor(None, None, self.index)
        self.assertEqual(editor.specialValueText(), "DEFAULT")


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)