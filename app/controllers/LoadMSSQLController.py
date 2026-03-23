import re
import math
from typing import override
from app.controllers.interfaces.LoadSQLControllerInterface import LoadSQLControllerInterface
from app.models.TableModel import TableModel
from app.models.RelationshipModel import RelationshipModel
from app.models.InheritanceModel import InheritanceModel
from app.enums.RelationshipsEnum import RelationshipsEnum


class LoadMSSQLController(LoadSQLControllerInterface):
    def __init__(self, MainWindowController, TablesModel, RelationshipsModel, InheritancesModel):
        self.__MainWindowController = MainWindowController
        self.__TablesModel = TablesModel
        self.__RelationshipsModel = RelationshipsModel
        self.__InheritancesModel = InheritancesModel
        self.__auto_place_count = 0

        self.__tables_by_name = {}
        self.__fk_constraints = {}
        self.__inheritances = []

        self.__DATA_TYPE_REVERSE_MAP = {
            "INT": "NUMBER",
            "INTEGER": "NUMBER",
            "SMALLINT": "NUMBER",
            "TINYINT": "NUMBER",
            "BIGINT": "NUMBER",
            "FLOAT": "FLOAT",
            "REAL": "FLOAT",
            "CHAR": "CHAR",
            "NCHAR": "NCHAR",
            "VARCHAR": "VARCHAR2",
            "NVARCHAR": "NVARCHAR2",
            "DATE": "DATE",
            "DATETIME": "DATE",
            "DATETIME2": "DATE",
            "SMALLDATETIME": "DATE",
            "TEXT": "CLOB",
            "NTEXT": "CLOB",
            "VARCHAR(MAX)": "CLOB",
            "NVARCHAR(MAX)": "CLOB",
            "VARBINARY": "BLOB",
            "VARBINARY(MAX)": "BLOB",
            "BINARY": "BLOB",
        }

    def __next_table_position(self, width=180, height=120, padding=30):
        n = self.__auto_place_count
        cols = max(1, math.ceil(math.sqrt(n + 1)))
        row = n // cols
        col = n % cols
        x = padding + col * (width + padding)
        y = padding + row * (height + padding)
        self.__auto_place_count += 1
        return x, y

    def __mapToOracleType(self, mssqlType: str) -> str:
        if not mssqlType:
            return mssqlType
        upper_type = mssqlType.upper().strip()
        base = upper_type.split('(')[0].strip()
        if base in ("VARCHAR", "NVARCHAR") and "MAX" in upper_type:
            key = f"{base}(MAX)"
            return self.__DATA_TYPE_REVERSE_MAP.get(key, base)
        return self.__DATA_TYPE_REVERSE_MAP.get(base, base)

    @override
    def parseSQLCode(self, sqlCode):
        self.__tables_by_name.clear()
        self.__fk_constraints.clear()
        self.__inheritances.clear()

        statements = [s.strip() for s in sqlCode.split(';') if s.strip()]
        for statement in statements:
            upper = statement.upper()
            if upper.startswith("CREATE TABLE"):
                self.__parseCreateTableSQL(statement + ';')
            elif upper.startswith("ALTER TABLE"):
                self.__parseRelationshipSQL(statement + ';')

        self.__buildInheritanceModelsFromFKs()
        self.__buildRelationshipsFromCreateTableFKs()

    def __parseCreateTableSQL(self, sql: str):
        m_table = re.search(r'CREATE\s+TABLE\s+\[([^]]+)\]', sql, re.IGNORECASE | re.DOTALL)
        if not m_table:
            m_table = re.search(r'CREATE\s+TABLE\s+([A-Za-z0-9_]+)', sql, re.IGNORECASE | re.DOTALL)
        if not m_table:
            return
        table_name = m_table.group(1)

        m_body = re.search(
            r'CREATE\s+TABLE\s+.+?\s*\((.*)\)\s*;',
            sql,
            re.IGNORECASE | re.DOTALL
        )
        body = m_body.group(1) if m_body else ""

        raw_lines = [l.strip() for l in self.__split_columns(body) if l.strip()]

        x, y = self.__next_table_position()
        table_model = TableModel(x + 100, y + 100, 100, 20, 5, self.__TablesModel.tableNumber)
        table_model.editTableName(table_name)

        self.__TablesModel.tables.append(table_model)
        self.__TablesModel.tableNumber += 1
        self.__tables_by_name[table_name] = table_model

        cols_model = table_model.getTableColumnsModel()

        pk_columns = set()
        unique_columns = set()
        fk_list = []
        parent_candidate = None

        for line in raw_lines:
            upper = line.upper()

            if upper.startswith("CONSTRAINT") or upper.startswith("PRIMARY KEY") or upper.startswith("UNIQUE") or upper.startswith("FOREIGN KEY"):
                m_pk = re.search(r'PRIMARY\s+KEY\s*\(([^)]+)\)', line, re.IGNORECASE)
                if m_pk:
                    cols = [c.strip().strip('[').strip(']').strip('"') for c in m_pk.group(1).split(',')]
                    for c in cols:
                        pk_columns.add(c)

                m_uniq = re.search(r'UNIQUE\s+.*\(([^)]+)\)', line, re.IGNORECASE)
                if m_uniq:
                    cols = [c.strip().strip('[').strip(']').strip('"') for c in m_uniq.group(1).split(',')]
                    for c in cols:
                        unique_columns.add(c)

                m_fk = re.search(
                    r'FOREIGN\s+KEY\s*\(\s*\[([^]]+)\]\s*\)\s+REFERENCES\s+\[([^]]+)\]\s*\(\s*\[([^]]+)\]\s*\)',
                    line,
                    re.IGNORECASE
                )
                if not m_fk:
                    m_fk = re.search(
                        r'FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+([A-Za-z0-9_]+)\s*\(([^)]+)\)',
                        line,
                        re.IGNORECASE
                    )
                if m_fk:
                    local_cols_raw = m_fk.group(1)
                    ref_table = m_fk.group(2)
                    ref_cols_raw = m_fk.group(3)

                    local_cols = [c.strip().strip('[').strip(']').strip('"') for c in local_cols_raw.split(',')]
                    ref_cols = [c.strip().strip('[').strip(']').strip('"') for c in ref_cols_raw.split(',')]

                    for lc, rc in zip(local_cols, ref_cols):
                        fk_list.append(
                            {
                                "local_col": lc,
                                "ref_table": ref_table,
                                "ref_col": rc,
                            }
                        )
                continue

            m_col = re.match(
                r'\[?(?P<name>[A-Za-z0-9_]+)\]?\s+'
                r'(?P<type>[A-Za-z0-9_]+(?:\s*\(\s*\d+\s*(?:,\s*\d+)?\s*\))?(?:\s+MAX)?)'
                r'(?P<rest>.*)$',
                line,
                re.IGNORECASE
            )
            if not m_col:
                continue

            col_name = m_col.group("name")
            data_type_raw = m_col.group("type")
            rest = m_col.group("rest") or ""

            length_match = re.search(r'\(\s*(\d+)\s*(?:,\s*\d+)?\s*\)', data_type_raw)
            length = length_match.group(1) if length_match else None

            oracle_type = self.__mapToOracleType(data_type_raw)
            length_val = int(length) if length else 0
            not_null = bool(re.search(r'\bNOT\s+NULL\b', rest, re.IGNORECASE))
            unique_inline = bool(re.search(r'\bUNIQUE\b', rest, re.IGNORECASE))

            cols_model.addColumn(
                columnName=col_name,
                dataType=oracle_type,
                length=length_val,
                unique=unique_inline,
                notNull=not_null,
                pk=False,
                fk=False,
            )

        if fk_list:
            self.__fk_constraints[table_name] = fk_list

        for fk in fk_list:
            if fk["ref_table"] != table_name:
                parent_candidate = fk["ref_table"]
                break

        if parent_candidate:
            self.__inheritances.append((table_name, parent_candidate))

        for column in cols_model.getColumns():
            name = column["columnName"]
            if name in pk_columns:
                column["pk"] = True
                column["notNull"] = True
            if name in unique_columns:
                column["unique"] = True

        table_model.changeTableDimensions()

    def __split_columns(self, body: str):
        parts = []
        current = []
        depth = 0
        for ch in body:
            if ch == '(':
                depth += 1
                current.append(ch)
            elif ch == ')':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                parts.append(''.join(current).strip())
                current = []
            else:
                current.append(ch)
        if current:
            parts.append(''.join(current).strip())
        return parts

    def __buildInheritanceModelsFromFKs(self):
        for child_name, parent_name in self.__inheritances:
            child_table = self.__tables_by_name.get(child_name)
            parent_table = self.__tables_by_name.get(parent_name)
            if not child_table or not parent_table:
                continue
            inheritance_model = InheritanceModel(child_table, parent_table)
            self.__InheritancesModel.addInheritanceModel(inheritance_model)

    def __parseRelationshipSQL(self, sql: str):
        m_table = re.search(r'ALTER\s+TABLE\s+\[([^]]+)\]', sql, re.IGNORECASE)
        if not m_table:
            m_table = re.search(r'ALTER\s+TABLE\s+([A-Za-z0-9_]+)', sql, re.IGNORECASE)
        if not m_table:
            return
        second_table_name = m_table.group(1)

        m_fk = re.search(r'FOREIGN\s+KEY\s*\(\s*\[([^]]+)\]\s*\)', sql, re.IGNORECASE)
        if not m_fk:
            m_fk = re.search(r'FOREIGN\s+KEY\s*\(([^)]+)\)', sql, re.IGNORECASE)
        m_ref = re.search(r'REFERENCES\s+\[([^]]+)\]\s*\(\s*\[([^]]+)\]\s*\)', sql, re.IGNORECASE)
        if not m_ref:
            m_ref = re.search(r'REFERENCES\s+([A-Za-z0-9_]+)\s*\(([^)]+)\)', sql, re.IGNORECASE)

        if not m_fk or not m_ref:
            return

        second_column_name = m_fk.group(1).split(',')[0].strip().strip('[').strip(']').strip('"')
        first_table_name = m_ref.group(1)
        first_column_name = m_ref.group(2).split(',')[0].strip().strip('[').strip(']').strip('"')

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

    def __buildRelationshipsFromCreateTableFKs(self):
        tables_to_remove = set()

        for table_name, fk_list in self.__fk_constraints.items():
            table_model = self.__tables_by_name.get(table_name)
            if not table_model:
                continue

            if len(fk_list) == 2:
                fk1, fk2 = fk_list
                if fk1["ref_table"] != fk2["ref_table"]:
                    first_table = self.__tables_by_name.get(fk1["ref_table"])
                    second_table = self.__tables_by_name.get(fk2["ref_table"])
                    if first_table and second_table:
                        first_cols_model = first_table.getTableColumnsModel()
                        second_cols_model = second_table.getTableColumnsModel()

                        for col in first_cols_model.getColumns():
                            if col["columnName"] == fk1["ref_col"]:
                                col["fk"] = True
                                break

                        for col in second_cols_model.getColumns():
                            if col["columnName"] == fk2["ref_col"]:
                                col["fk"] = True
                                break

                        rel = RelationshipModel(
                            first_table,
                            second_table,
                            fk1["ref_col"],
                            fk2["ref_col"],
                            RelationshipsEnum.REL_n_n
                        )
                        self.__RelationshipsModel.addRelationship(rel)

                        tables_to_remove.add(table_name)
                        continue

            for fk in fk_list:
                first_table = self.__tables_by_name.get(fk["ref_table"])
                second_table = table_model
                if not first_table or not second_table:
                    continue

                second_column_name = fk["local_col"]
                first_column_name = fk["ref_col"]

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

                rel_model = RelationshipModel(
                    first_table,
                    second_table,
                    first_column_name,
                    second_column_name,
                    rel_type
                )
                self.__RelationshipsModel.addRelationship(rel_model)

        if tables_to_remove:
            self.__TablesModel.tables = [
                t for t in self.__TablesModel.tables
                if t.getTableName() not in tables_to_remove
            ]
            for name in tables_to_remove:
                self.__tables_by_name.pop(name, None)

    def __isOneToOneRelationship(self, firstTable, secondTable, firstColumnName, secondColumnName):
        cols = secondTable.getTableColumnsModel().getColumns()
        for col in cols:
            if col["columnName"] == secondColumnName:
                return bool(col.get("unique") or col.get("pk"))
        return False
