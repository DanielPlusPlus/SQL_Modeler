from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.models.TableModel import TableModel
from app.models.RelationshipModel import RelationshipModel
from app.models.InheritanceModel import InheritanceModel
from app.enums.RelationshipsEnum import RelationshipsEnum

import re
import math


class LoadSQLController:
    def __init__(self, ParentWindow, MainWindowController, TablesModel, RelationshipsModel, InheritancesModel):
        self.__ParentWindow = ParentWindow
        self.__MainWindowController = MainWindowController
        self.__TablesModel: TablesModel = TablesModel
        self.__RelationshipsModel = RelationshipsModel
        self.__InheritancesModel = InheritancesModel
        self.__auto_place_count = 0

        self.__tables_by_name = {}
        self.__types_by_name = {}

    def __next_table_position(self, width=180, height=120, padding=30):
        n = self.__auto_place_count
        cols = max(1, math.ceil(math.sqrt(n + 1)))
        row = n // cols
        col = n % cols
        x = padding + col * (width + padding)
        y = padding + row * (height + padding)
        self.__auto_place_count += 1
        return x, y

    def parseSQLCode(self, sqlCode: str):
        self.__tables_by_name.clear()
        self.__types_by_name.clear()

        statements = [s.strip() for s in sqlCode.split(';') if s.strip()]
        for statement in statements:
            upper = statement.upper()
            if upper.startswith("CREATE TABLE"):
                self.__parseCreateTableSQL(statement + ';')
            elif upper.startswith("CREATE OR REPLACE TYPE"):
                self.__parseInheritanceSQL(statement + ';')
            elif upper.startswith("ALTER TABLE"):
                self.__parseRelationshipSQL(statement + ';')

        self.__buildInheritanceModelsFromTypes()

    def __parseCreateTableSQL(self, sql: str):
        m_table = re.search(r'CREATE\s+TABLE\s+"([^"]+)"', sql, re.IGNORECASE | re.DOTALL)
        if not m_table:
            return
        table_name = m_table.group(1)

        m_of_type = re.search(r'CREATE\s+TABLE\s+"[^"]+"\s+OF\s+"([^"]+)"', sql, re.IGNORECASE | re.DOTALL)
        of_type_name = m_of_type.group(1) if m_of_type else None

        m_body = re.search(r'CREATE\s+TABLE\s+".+?"(?:\s+OF\s+".+?")?\s*\((.*)\)\s*;', sql,
                           re.IGNORECASE | re.DOTALL)
        body = m_body.group(1) if m_body else ""


        raw_lines = [l.strip() for l in body.split(',') if l.strip()]


        x, y = self.__next_table_position()
        table_model = TableModel(x + 100, y + 100, 100, 20, 5, self.__TablesModel.tableNumber)
        table_model.editTableName(table_name)


        self.__TablesModel.tables.append(table_model)
        self.__TablesModel.tableNumber += 1
        self.__tables_by_name[table_name] = table_model

        cols_model = table_model.getTableColumnsModel()


        pk_columns = set()
        unique_columns = set()

        for line in raw_lines:
            upper = line.upper()
            if upper.startswith("CONSTRAINT") or upper.startswith("PRIMARY KEY") or upper.startswith("UNIQUE"):
                m_pk = re.search(r'PRIMARY\s+KEY\s*\(([^)]+)\)', line, re.IGNORECASE)
                if m_pk:
                    cols = [c.strip().strip('"') for c in m_pk.group(1).split(',')]
                    for c in cols:
                        pk_columns.add(c)
                m_uniq = re.search(r'UNIQUE\s*\(([^)]+)\)', line, re.IGNORECASE)
                if m_uniq:
                    cols = [c.strip().strip('"') for c in m_uniq.group(1).split(',')]
                    for c in cols:
                        unique_columns.add(c)
                continue

            m_col = re.match(
                r'"(?P<name>[^"]+)"\s+'
                r'(?P<type>[A-Z0-9_]+)'
                r'(?:\((?P<len>\d+)\))?'
                r'(?P<rest>.*)$',
                line,
                re.IGNORECASE
            )
            if not m_col:
                continue

            col_name = m_col.group("name")
            data_type = m_col.group("type")
            length = m_col.group("len")
            rest = m_col.group("rest") or ""

            length_val = int(length) if length else 0
            not_null = bool(re.search(r'\bNOT\s+NULL\b', rest, re.IGNORECASE))
            unique_inline = bool(re.search(r'\bUNIQUE\b', rest, re.IGNORECASE))


            cols_model.addColumn(
                columnName=col_name,
                dataType=data_type,
                length=length_val,
                unique=unique_inline,
                notNull=not_null,
                pk=False,
                fk=False
            )

        for column in cols_model.getColumns():
            name = column["columnName"]
            if name in pk_columns:
                column["pk"] = True
                column["notNull"] = True
            if name in unique_columns:
                column["unique"] = True

        table_model.changeTableDimensions()

    def __parseInheritanceSQL(self, sql: str):
        m_type = re.search(r'CREATE\s+OR\s+REPLACE\s+TYPE\s+"([^"]+)"', sql,
                           re.IGNORECASE | re.DOTALL)
        if not m_type:
            return
        type_name = m_type.group(1)

        m_under = re.search(r'UNDER\s+"([^"]+)"', sql, re.IGNORECASE | re.DOTALL)
        parent_type = m_under.group(1) if m_under else None

        m_body = re.search(
            r'AS\s+OBJECT\s*\((.*)\)\s*NOT\s+FINAL'
            r'|UNDER\s+".+?"\s*\((.*)\)\s*;',
            sql,
            re.IGNORECASE | re.DOTALL
        )

        body = ""
        if m_body:
            body = m_body.group(1) if m_body.group(1) is not None else m_body.group(2)

        raw_lines = [l.strip() for l in body.split(',') if l.strip()]

        columns = []
        for line in raw_lines:
            m_col = re.match(
                r'"(?P<name>[^"]+)"\s+'
                r'(?P<type>[A-Z0-9_]+)'
                r'(?:\((?P<len>\d+)\))?',
                line,
                re.IGNORECASE
            )
            if not m_col:
                continue
            col_name = m_col.group("name")
            data_type = m_col.group("type")
            length = m_col.group("len")
            length_val = int(length) if length else 0

            columns.append(
                {
                    "columnName": col_name,
                    "dataType": data_type,
                    "length": length_val,
                    "unique": False,
                    "notNull": False,
                    "pk": False,
                    "fk": False,
                }
            )

        self.__types_by_name[type_name] = {
            "name": type_name,
            "parent": parent_type,
            "columns": columns,
        }

    def __buildInheritanceModelsFromTypes(self):
        type_to_table = {}
        for table in self.__TablesModel.getTables():
            tname = table.getTableName()
            type_name = f"{tname}_T"
            type_to_table[type_name] = table

        for type_name, info in self.__types_by_name.items():
            table = type_to_table.get(type_name)
            if not table:
                continue
            cols_model = table.getTableColumnsModel()
            cols_model._TableColumnsModel__columns.clear()

        for type_name, info in self.__types_by_name.items():
            parent_type = info["parent"]
            if parent_type:
                continue

            base_table = type_to_table.get(type_name)
            if not base_table:
                continue

            base_cols = info.get("columns", [])
            base_cols_model = base_table.getTableColumnsModel()

            for col in base_cols:
                base_cols_model.addColumn(
                    col["columnName"],
                    col["dataType"],
                    col["length"],
                    col["unique"],
                    col["notNull"],
                    col["pk"],
                    col["fk"],
                )
            base_table.changeTableDimensions()

        for type_name, info in self.__types_by_name.items():
            parent_type = info["parent"]
            if not parent_type:
                continue

            child_table = type_to_table.get(type_name)
            if not child_table:
                continue

            child_cols_only = info.get("columns", [])
            child_cols_model = child_table.getTableColumnsModel()

            for col in child_cols_only:
                child_cols_model.addColumn(
                    col["columnName"],
                    col["dataType"],
                    col["length"],
                    col["unique"],
                    col["notNull"],
                    col["pk"],
                    col["fk"],
                )
            child_table.changeTableDimensions()

        for type_name, info in self.__types_by_name.items():
            parent_type = info["parent"]
            if not parent_type:
                continue

            child_table = type_to_table.get(type_name)
            parent_table = type_to_table.get(parent_type)
            if not child_table or not parent_table:
                continue

            inheritance_model = InheritanceModel(child_table, parent_table)
            self.__InheritancesModel.addInheritanceModel(inheritance_model)

    def __parseRelationshipSQL(self, sql: str):
        m_table = re.search(r'ALTER\s+TABLE\s+"([^"]+)"', sql, re.IGNORECASE)
        if not m_table:
            return
        second_table_name = m_table.group(1)

        m_fk = re.search(r'FOREIGN\s+KEY\s*\("([^"]+)"\)', sql, re.IGNORECASE)
        m_ref = re.search(r'REFERENCES\s+"([^"]+)"\s*\("([^"]+)"\)', sql, re.IGNORECASE)

        if not m_fk or not m_ref:
            return

        second_column_name = m_fk.group(1)
        first_table_name = m_ref.group(1)
        first_column_name = m_ref.group(2)

        first_table = self.__tables_by_name.get(first_table_name)
        second_table = self.__tables_by_name.get(second_table_name)
        if not first_table or not second_table:
            return

        cols_model = second_table.getTableColumnsModel()
        for col in cols_model.getColumns():
            if col["columnName"] == second_column_name:
                if col.get("pk") or col.get("unique"):
                    break
                col["fk"] = True
                break

        if self.__isOneToOneRelationship(first_table, second_table, first_column_name, second_column_name):
            rel_type = RelationshipsEnum.REL_1_1
        else:
            rel_type = RelationshipsEnum.REL_1_n

        relationship_model = RelationshipModel(
            first_table,
            second_table,
            first_column_name,
            second_column_name,
            rel_type
        )
        self.__RelationshipsModel.addRelationship(relationship_model)

    def __isOneToOneRelationship(self, firstTable, secondTable, firstColumnName, secondColumnName):
        cols = secondTable.getTableColumnsModel().getColumns()
        for col in cols:
            if col["columnName"] == secondColumnName:
                return bool(col.get("unique") or col.get("pk"))
        return False

    def openFileDialogAndProcessSQL(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.__ParentWindow,
            "Select SQL File",
            "",
            "SQL Files (*.sql);;All Files (*)"
        )

        if filePath:
            try:
                with open(filePath, "r", encoding="utf-8") as file:
                    sqlCode = file.read()

                self.parseSQLCode(sqlCode)

                QMessageBox.information(
                    self.__ParentWindow,
                    "Success",
                    "SQL file successfully processed!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self.__ParentWindow,
                    "Error",
                    f"An error occurred while processing the file: {str(e)}"
                )