import unittest
from unittest.mock import MagicMock, patch

from app.controllers.GenerateSQLController import GenerateSQLController
from app.enums.RelationshipsEnum import RelationshipsEnum


class TestGenerateSQLController(unittest.TestCase):

    def setUp(self):
        self.parentWindow = MagicMock()
        self.mainWindowController = MagicMock()

        self.tablesModel = MagicMock()
        self.relationshipsModel = MagicMock()
        self.inheritancesModel = MagicMock()

        self.controller = GenerateSQLController(
            self.parentWindow,
            self.mainWindowController,
            self.tablesModel,
            self.relationshipsModel,
            self.inheritancesModel
        )

    def testGenerateCreateTableSQLCodeGeneratesCorrectSql(self):
        mockTable = MagicMock()
        mockTable.getTableName.return_value = "Person"
        mockTable.getTableColumns.return_value = [
            {"columnName": "id", "dataType": "NUMBER", "length": None, "notNull": True, "unique": True, "pk": True},
            {"columnName": "name", "dataType": "VARCHAR2", "length": 100, "notNull": False, "unique": False,
             "pk": False},
        ]

        sql = self.controller._GenerateSQLController__generateCreateTableSQLCode(mockTable)

        expected = (
            'CREATE TABLE "Person" (\n'
            '    "id" NUMBER NOT NULL UNIQUE,\n'
            '    "name" VARCHAR2(100),\n'
            '    CONSTRAINT "pk_Person" PRIMARY KEY ("id")\n'
            ');'
        )
        self.assertEqual(sql, expected)

    def testGenerateCreateTableFromTypeSQLCodeGeneratesCorrectSql(self):
        mockTable = MagicMock()
        mockTable.getTableName.return_value = "Employee"
        mockTable.getTableColumns.return_value = [
            {"columnName": "id", "pk": True, "notNull": True, "unique": False},
            {"columnName": "position", "pk": False, "notNull": False, "unique": True},
        ]

        sql = self.controller._GenerateSQLController__generateCreateTableFromTypeSQLCode(mockTable)

        expected = (
            'CREATE TABLE "Employee" OF "Employee_T" (\n'
            '    "id" NOT NULL,\n'
            '    UNIQUE ("position"),\n'
            '    CONSTRAINT "pk_Employee" PRIMARY KEY ("id")\n'
            ');'
        )
        self.assertEqual(sql, expected)

    def testGenerateInheritanceTypeSQLCodeGeneratesCorrectSql(self):
        child = MagicMock()
        parent = MagicMock()
        child.getTableName.return_value = "Employee"
        parent.getTableName.return_value = "Person"
        parent.getTableColumns.return_value = [
            {"columnName": "id", "dataType": "NUMBER", "length": None},
            {"columnName": "name", "dataType": "VARCHAR2", "length": 100}
        ]
        child.getTableColumns.return_value = [
            {"columnName": "id", "dataType": "NUMBER", "length": None},
            {"columnName": "name", "dataType": "VARCHAR2", "length": 100},
            {"columnName": "salary", "dataType": "NUMBER", "length": None}
        ]

        inheritance = MagicMock()
        inheritance.getFirstTable.return_value = child
        inheritance.getSecondTable.return_value = parent

        sql = self.controller._GenerateSQLController__generateInheritanceTypeSQLCode(inheritance)

        self.assertIn('CREATE OR REPLACE TYPE "Person_T"', sql)
        self.assertIn('CREATE OR REPLACE TYPE "Employee_T" UNDER "Person_T"', sql)

    def testGenerateRelationshipSQLCodeFor1NRelationship(self):
        relationship = MagicMock()
        relationship.getRelationshipType.return_value = RelationshipsEnum.REL_1_n

        firstTable = MagicMock()
        secondTable = MagicMock()
        firstTable.getTableName.return_value = "Department"
        secondTable.getTableName.return_value = "Employee"
        relationship.getFirstTable.return_value = firstTable
        relationship.getSecondTable.return_value = secondTable

        relationship.getFirstSelectedColumnName.return_value = "id"
        relationship.getSecondSelectedColumnName.return_value = "dept_id"

        sql = self.controller._GenerateSQLController__generateRelationshipSQLCode(relationship)

        expected = (
            'ALTER TABLE "Employee" ADD CONSTRAINT "fk_Employee_dept_id" '
            'FOREIGN KEY ("dept_id") REFERENCES "Department"("id");'
        )
        self.assertEqual(sql, expected)

    def testGenerateCreateJunctionTableSQLCodeForNNRelationship(self):
        relationship = MagicMock()
        relationship.getRelationshipType.return_value = RelationshipsEnum.REL_n_n

        firstTable = MagicMock()
        secondTable = MagicMock()
        firstTable.getTableName.return_value = "Student"
        secondTable.getTableName.return_value = "Course"
        relationship.getFirstTable.return_value = firstTable
        relationship.getSecondTable.return_value = secondTable

        relationship.getFirstSelectedColumnName.return_value = "student_id"
        relationship.getSecondSelectedColumnName.return_value = "course_id"

        sql = self.controller._GenerateSQLController__generateCreateJunctionTableSQLCode(relationship)

        self.assertIn('CREATE TABLE "Student_Course"', sql)
        self.assertIn('CONSTRAINT "pk_Student_Course"', sql)
        self.assertIn(
            'CONSTRAINT "fk_Student_Course_Student" FOREIGN KEY ("Student_student_id") REFERENCES "Student"("student_id")',
            sql
        )

    def testGenerateSQLCodeIntegration(self):
        mockTable = MagicMock()
        mockTable.getTableName.return_value = "Person"
        mockTable.getTableColumns.return_value = []

        mockInheritance = MagicMock()
        mockInheritance.getFirstTable.return_value = mockTable
        mockInheritance.getSecondTable.return_value = mockTable
        self.inheritancesModel.getInheritances.return_value = [mockInheritance]

        self.tablesModel.getTables.return_value = [mockTable]
        self.relationshipsModel.getRelationships.return_value = []

        sql = self.controller._GenerateSQLController__generateSQLCode()

        self.assertIn("CREATE OR REPLACE TYPE", sql)
        self.assertIn("CREATE TABLE", sql)

    @patch("app.controllers.GenerateSQLController.GenerateSQLDialogView")
    @patch("app.controllers.GenerateSQLController.GenerateSQLDialogController")
    def testDisplayDialogCallsAllDependencies(self, mockControllerClass, mockViewClass):
        mockDialogInstance = MagicMock()
        mockViewClass.return_value = mockDialogInstance

        self.controller._GenerateSQLController__generateSQLCode = MagicMock(return_value="SQL CODE")
        self.controller.displayDialog()

        mockViewClass.assert_called_once_with(self.parentWindow)
        mockDialogInstance.setupUI.assert_called_once_with("SQL CODE")
        mockControllerClass.assert_called_once_with(self.parentWindow, self.mainWindowController, mockDialogInstance)
        mockDialogInstance.displayDialog.assert_called_once()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
