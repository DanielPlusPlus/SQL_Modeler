import unittest
from unittest.mock import MagicMock, patch, mock_open
from PySide6.QtWidgets import QApplication, QWidget

from app.controllers.LoadSQLController import LoadSQLController
from app.enums.RelationshipsEnum import RelationshipsEnum

app = QApplication.instance() or QApplication([])


class DummyTablesModel:
    def __init__(self):
        self.tables = []
        self.tableNumber = 1

    def getTables(self):
        return self.tables


class DummyRelationshipsModel:
    def __init__(self):
        self.relationships = []

    def addRelationship(self, rel):
        self.relationships.append(rel)


class DummyInheritancesModel:
    def __init__(self):
        self.inheritances = []

    def addInheritanceModel(self, inh):
        self.inheritances.append(inh)


class TestLoadSQLController(unittest.TestCase):
    def setUp(self):
        self.parent = QWidget()
        self.mainWindowController = MagicMock()
        self.tablesModel = DummyTablesModel()
        self.relationshipsModel = DummyRelationshipsModel()
        self.inheritancesModel = DummyInheritancesModel()

        self.controller = LoadSQLController(
            self.parent,
            self.mainWindowController,
            self.tablesModel,
            self.relationshipsModel,
            self.inheritancesModel,
        )

    def test_parse_create_table_simple(self):
        sql = '''
        CREATE TABLE "EMP" (
            "ID" NUMBER(10) PRIMARY KEY,
            "NAME" VARCHAR2(50) NOT NULL,
            "EMAIL" VARCHAR2(100) UNIQUE
        );
        '''

        self.controller.parseSQLCode(sql)

        self.assertEqual(len(self.tablesModel.tables), 1)
        table = self.tablesModel.tables[0]

        self.assertEqual(table.getTableName(), "EMP")

        cols_model = table.getTableColumnsModel()
        cols = cols_model.getColumns()
        self.assertEqual(len(cols), 3)

        id_col = next(c for c in cols if c["columnName"] == "ID")
        name_col = next(c for c in cols if c["columnName"] == "NAME")
        email_col = next(c for c in cols if c["columnName"] == "EMAIL")

        self.assertEqual(id_col["dataType"].upper(), "NUMBER")
        self.assertEqual(id_col["length"], 10)
        self.assertFalse(id_col["pk"])
        self.assertFalse(id_col["notNull"])

        self.assertEqual(name_col["dataType"].upper(), "VARCHAR2")
        self.assertEqual(name_col["length"], 50)
        self.assertTrue(name_col["notNull"])
        self.assertFalse(name_col["pk"])

        self.assertEqual(email_col["dataType"].upper(), "VARCHAR2")
        self.assertEqual(email_col["length"], 100)
        self.assertTrue(email_col["unique"])

    def test_parse_multiple_tables_and_auto_positioning(self):
        sql = '''
        CREATE TABLE "T1" ("ID" NUMBER(10));
        CREATE TABLE "T2" ("ID" NUMBER(10));
        CREATE TABLE "T3" ("ID" NUMBER(10));
        '''

        self.controller.parseSQLCode(sql)

        self.assertEqual(len(self.tablesModel.tables), 3)
        names = [t.getTableName() for t in self.tablesModel.tables]
        self.assertEqual(names, ["T1", "T2", "T3"])

        rects = [t.getRectangle() for t in self.tablesModel.tables]
        centers = {(r.center().x(), r.center().y()) for r in rects}
        self.assertGreater(len(centers), 1)

    def test_parse_inheritance_types_and_build_models(self):
        sql = '''
        CREATE OR REPLACE TYPE "PERSON_T" AS OBJECT(
            "ID" NUMBER(10),
            "NAME" VARCHAR2(50)
        ) NOT FINAL;

        CREATE OR REPLACE TYPE "EMP_T" UNDER "PERSON_T"(
            "SALARY" NUMBER(10)
        );

        CREATE TABLE "PERSON" OF "PERSON_T" (
            CONSTRAINT PERSON_PK PRIMARY KEY ("ID")
        );

        CREATE TABLE "EMP" OF "EMP_T" (
            CONSTRAINT EMP_PK PRIMARY KEY ("ID")
        );
        '''

        self.controller.parseSQLCode(sql)

        self.assertEqual(len(self.tablesModel.tables), 2)
        tables_by_name = {t.getTableName(): t for t in self.tablesModel.tables}
        self.assertIn("PERSON", tables_by_name)
        self.assertIn("EMP", tables_by_name)

        person = tables_by_name["PERSON"]
        emp = tables_by_name["EMP"]

        person_cols = [c["columnName"] for c in person.getTableColumnsModel().getColumns()]
        emp_cols = [c["columnName"] for c in emp.getTableColumnsModel().getColumns()]

        self.assertIn("ID", person_cols)
        self.assertIn("NAME", person_cols)
        self.assertEqual(emp_cols, ["SALARY"])

        self.assertEqual(len(self.inheritancesModel.inheritances), 1)
        inh = self.inheritancesModel.inheritances[0]
        self.assertEqual(inh.getFirstTable().getTableName(), "EMP")
        self.assertEqual(inh.getSecondTable().getTableName(), "PERSON")

    def test_parse_relationships_creates_1n_and_sets_fk(self):
        sql = '''
        CREATE TABLE "PARENT" (
            "ID" NUMBER(10) PRIMARY KEY
        );

        CREATE TABLE "CHILD" (
            "ID" NUMBER(10) PRIMARY KEY,
            "PARENT_ID" NUMBER(10)
        );

        ALTER TABLE "CHILD"
            ADD CONSTRAINT "CHILD_FK"
            FOREIGN KEY ("PARENT_ID")
            REFERENCES "PARENT" ("ID");
        '''

        self.controller.parseSQLCode(sql)

        self.assertEqual(len(self.tablesModel.tables), 2)
        tables_by_name = {t.getTableName(): t for t in self.tablesModel.tables}
        parent = tables_by_name["PARENT"]
        child = tables_by_name["CHILD"]

        self.assertEqual(len(self.relationshipsModel.relationships), 1)
        rel = self.relationshipsModel.relationships[0]

        self.assertIs(rel.getFirstTable(), parent)
        self.assertIs(rel.getSecondTable(), child)
        self.assertEqual(rel.getFirstSelectedColumnName(), "ID")
        self.assertEqual(rel.getSecondSelectedColumnName(), "PARENT_ID")
        self.assertEqual(rel.getRelationshipType(), RelationshipsEnum.REL_1_n)

        child_cols = child.getTableColumnsModel().getColumns()
        parent_id_col = next(c for c in child_cols if c["columnName"] == "PARENT_ID")
        self.assertTrue(parent_id_col["fk"])

    @patch("app.controllers.LoadSQLController.QFileDialog.getOpenFileName")
    @patch("app.controllers.LoadSQLController.QMessageBox.information")
    def test_openFileDialogAndProcessSQL_success(self, mockInfo, mockGetOpenFileName):
        mockGetOpenFileName.return_value = ("test.sql", "SQL Files (*.sql)")
        fake_sql = 'CREATE TABLE "T1" ("ID" NUMBER(10));'

        with patch("builtins.open", mock_open(read_data=fake_sql)) as m_open:
            self.controller.openFileDialogAndProcessSQL()

        mockGetOpenFileName.assert_called_once()
        m_open.assert_called_once_with("test.sql", "r", encoding="utf-8")
        mockInfo.assert_called_once()
        self.assertEqual(len(self.tablesModel.tables), 1)

    @patch("app.controllers.LoadSQLController.QFileDialog.getOpenFileName")
    @patch("app.controllers.LoadSQLController.QMessageBox.critical")
    def test_openFileDialogAndProcessSQL_error(self, mockCritical, mockGetOpenFileName):
        mockGetOpenFileName.return_value = ("test.sql", "SQL Files (*.sql)")

        with patch("builtins.open", side_effect=IOError("fail")):
            self.controller.openFileDialogAndProcessSQL()

        mockGetOpenFileName.assert_called_once()
        mockCritical.assert_called_once()


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)