from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtWidgets import (QComboBox, QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QSpinBox, QTableView, QWidget, QHeaderView)
from PySide6.QtGui import QRegularExpressionValidator
from app.views.delegates.LineEditDelegate import LineEditDelegate
from app.views.delegates.ComboBoxDelegate import ComboBoxDelegate
from app.views.delegates.SpinBoxDelegate import SpinBoxDelegate


class EditTableDialogView(QDialog):
    def __init__(self, ParentWindow, ObtainedTable):
        super().__init__(ParentWindow)
        self.__ObtainedTable = ObtainedTable
        self.__regex = QRegularExpression(r'^[A-Za-z_][A-Za-z0-9_$#\s]*$')
        self.__dataTypes = ["NUMBER", "FLOAT", "CHAR", "VARCHAR2", "NCHAR", "NVARCHAR2", "DATE", "CLOB", "BLOB"]

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"EditTableDialog")
        self.resize(740, 400)
        self.setWindowTitle(u"Edit Table")

        self.__gridLayout = QGridLayout(self)

        self.__horizontalLayout = QHBoxLayout()
        self.__tableNameLabel = QLabel(u"Table Name", self)
        self.__tableNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tableNameLineEdit = QLineEdit(self)
        validator = QRegularExpressionValidator(self.__regex, self.tableNameLineEdit)
        self.tableNameLineEdit.setValidator(validator)
        self.tableNameLineEdit.setMaxLength(30)
        self.tableNameLineEdit.setText(self.__ObtainedTable.getTableName())
        self.__horizontalLayout.addWidget(self.__tableNameLabel)
        self.__horizontalLayout.addWidget(self.tableNameLineEdit)
        self.__horizontalLayout.setStretch(0, 3)
        self.__horizontalLayout.setStretch(1, 7)
        self.__gridLayout.addLayout(self.__horizontalLayout, 0, 0, 1, 1)

        self.__horizontalLayout_2 = QHBoxLayout()
        self.__horizontalLayout_2.addStretch()
        self.__gridLayout.addLayout(self.__horizontalLayout_2, 0, 1, 1, 2)

        self.__horizontalLayout_3 = QHBoxLayout()
        self.__columnNameLabel = QLabel(u"Column Name", self)
        self.__columnNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.columnNameLineEdit = QLineEdit(self)
        validator = QRegularExpressionValidator(self.__regex, self.columnNameLineEdit)
        self.columnNameLineEdit.setValidator(validator)
        self.columnNameLineEdit.setMaxLength(30)
        self.__horizontalLayout_3.addWidget(self.__columnNameLabel)
        self.__horizontalLayout_3.addWidget(self.columnNameLineEdit)
        self.__horizontalLayout_3.setStretch(0, 3)
        self.__horizontalLayout_3.setStretch(1, 7)
        self.__gridLayout.addLayout(self.__horizontalLayout_3, 1, 0, 1, 1)

        self.__horizontalLayout_4 = QHBoxLayout()
        self.__dataTypeLabel = QLabel(u"Data Type", self)
        self.__dataTypeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dataTypeComboBox = QComboBox(self)
        self.dataTypeComboBox.addItems(self.__dataTypes)
        self.__horizontalLayout_4.addWidget(self.__dataTypeLabel)
        self.__horizontalLayout_4.addWidget(self.dataTypeComboBox)
        self.__horizontalLayout_4.setStretch(0, 5)
        self.__horizontalLayout_4.setStretch(1, 5)
        self.__gridLayout.addLayout(self.__horizontalLayout_4, 1, 1, 1, 1)

        self.__horizontalLayout_5 = QHBoxLayout()
        self.__lengthLabel = QLabel(u"Length", self)
        self.__lengthLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lengthSpinBox = QSpinBox(self)
        self.lengthSpinBox.setRange(0, 4000)
        self.lengthSpinBox.setSpecialValueText("DEFAULT")
        self.__horizontalLayout_5.addWidget(self.__lengthLabel)
        self.__horizontalLayout_5.addWidget(self.lengthSpinBox)
        self.__horizontalLayout_5.setStretch(0, 5)
        self.__horizontalLayout_5.setStretch(1, 5)
        self.__gridLayout.addLayout(self.__horizontalLayout_5, 1, 2, 1, 1)

        self.__horizontalLayout_7 = QHBoxLayout()
        self.tableView = QTableView(self)
        self.tableView.setFrameShape(QFrame.Shape.StyledPanel)
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tableView.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.tableView.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.tableView.setModel(self.__ObtainedTable.getTableColumnsModel())
        ColumnNameDelegate = LineEditDelegate(self.__regex, 30, self.tableView)
        DataTypesComboDelegate = ComboBoxDelegate(self.__dataTypes, self.tableView)
        LengthSpinBoxDelegate = SpinBoxDelegate(0, 4000, self.tableView)

        self.tableView.setItemDelegateForColumn(0, ColumnNameDelegate)
        self.tableView.setItemDelegateForColumn(1, DataTypesComboDelegate)
        self.tableView.setItemDelegateForColumn(2, LengthSpinBoxDelegate)
        header = self.tableView.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.__horizontalLayout_7.addWidget(self.tableView)
        self.__gridLayout.addLayout(self.__horizontalLayout_7, 2, 0, 1, 3)

        self.__horizontalLayout_8 = QHBoxLayout()
        self.addColumnButton = QPushButton(u"Add Column", self)
        self.deleteColumnButton = QPushButton(u"Delete Selected Column", self)
        self.editColumnButton = QPushButton(u"Enable Editing Mode", self)
        self.__horizontalLayout_8.addWidget(self.addColumnButton)
        self.__horizontalLayout_8.addWidget(self.deleteColumnButton)
        self.__horizontalLayout_8.addWidget(self.editColumnButton)
        self.__horizontalLayout_8.setStretch(0, 1)
        self.__horizontalLayout_8.setStretch(1, 1)
        self.__horizontalLayout_8.setStretch(2, 1)
        self.__gridLayout.addLayout(self.__horizontalLayout_8, 3, 0, 1, 3)

        self.__horizontalLayout_9 = QHBoxLayout()
        self.__horizontalLayout_10 = QHBoxLayout()
        self.__horizontalLayout_11 = QHBoxLayout()
        self.__horizontalLayout_12 = QHBoxLayout()
        self.__pleceholderWidget = QWidget(self)
        self.cancelButton = QPushButton(u"Cancel", self)
        self.okButton = QPushButton(u"OK", self)
        self.__horizontalLayout_10.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_11.addWidget(self.__pleceholderWidget)
        self.__horizontalLayout_12.addWidget(self.cancelButton)
        self.__horizontalLayout_12.addWidget(self.okButton)
        self.__horizontalLayout_9.addLayout(self.__horizontalLayout_10)
        self.__horizontalLayout_9.addLayout(self.__horizontalLayout_11)
        self.__horizontalLayout_9.addLayout(self.__horizontalLayout_12)
        self.__horizontalLayout_9.setStretch(0, 1)
        self.__horizontalLayout_9.setStretch(1, 1)
        self.__horizontalLayout_9.setStretch(2, 1)
        self.__gridLayout.addLayout(self.__horizontalLayout_9, 4, 0, 1, 3)

        self.__gridLayout.setRowStretch(0, 1)
        self.__gridLayout.setRowStretch(1, 1)
        self.__gridLayout.setRowStretch(2, 6)
        self.__gridLayout.setRowStretch(3, 1)
        self.__gridLayout.setRowStretch(4, 1)
        self.__gridLayout.setColumnStretch(0, 5)
        self.__gridLayout.setColumnStretch(1, 3)
        self.__gridLayout.setColumnStretch(2, 2)

    def displayDialog(self):
        result = self.exec()
        return result
