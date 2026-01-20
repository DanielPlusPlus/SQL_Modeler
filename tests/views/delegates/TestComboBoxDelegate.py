import sys
import unittest
from PySide6.QtWidgets import QApplication, QComboBox, QWidget
from PySide6.QtCore import Qt, QModelIndex
from unittest.mock import MagicMock

from app.views.delegates.ComboBoxDelegate import ComboBoxDelegate

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


class TestComboBoxDelegate(unittest.TestCase):
    def setUp(self):
        self.dataTypes = ["int", "varchar", "bool"]
        self.delegate = ComboBoxDelegate(self.dataTypes)

    def testCreateEditor(self):
        parent = QWidget()
        editor = self.delegate.createEditor(parent, None, None)
        self.assertIsInstance(editor, QComboBox)
        self.assertEqual(editor.count(), len(self.dataTypes))
        for i, item in enumerate(self.dataTypes):
            self.assertEqual(editor.itemText(i), item)

    def testSetEditorDataSetsCorrectIndex(self):
        model = MagicMock()
        index = MagicMock(spec=QModelIndex)
        index.model.return_value = model
        model.data.return_value = "varchar"

        editor = QComboBox()
        editor.addItems(self.dataTypes)

        self.delegate.setEditorData(editor, index)
        self.assertEqual(editor.currentText(), "varchar")

    def testSetEditorDataValueNotFound(self):
        model = MagicMock()
        index = MagicMock(spec=QModelIndex)
        index.model.return_value = model
        model.data.return_value = "not_in_list"

        editor = QComboBox()
        editor.addItems(self.dataTypes)

        self.delegate.setEditorData(editor, index)
        self.assertEqual(editor.currentIndex(), 0)

    def testSetModelDataCallsSetData(self):
        model = MagicMock()
        index = MagicMock(spec=QModelIndex)

        editor = QComboBox()
        editor.addItems(self.dataTypes)
        editor.setCurrentIndex(1)

        self.delegate.setModelData(editor, model, index)
        model.setData.assert_called_once_with(index, "varchar", Qt.EditRole)


if __name__ == "__main__":
    unittest.main()
