from typing import override
from app.controllers.interfaces.GenerateSQLControllerInterface import GenerateSQLControllerInterface
from app.enums.RelationshipsEnum import RelationshipsEnum


class GeneratePostgreSQLController(GenerateSQLControllerInterface):
    def __init__(self, TablesModel, RelationshipsModel, InheritancesModel):
        self.__TablesModel = TablesModel
        self.__RelationshipsModel = RelationshipsModel
        self.__InheritancesModel = InheritancesModel
        self.__DATA_TYPE_MAP = {
            "NUMBER": "INTEGER",
            "FLOAT": "DOUBLE PRECISION",
            "CHAR": "CHAR",
            "VARCHAR2": "VARCHAR",
            "NCHAR": "CHAR",
            "NVARCHAR2": "VARCHAR",
            "DATE": "DATE",
            "CLOB": "TEXT",
            "BLOB": "BYTEA",
        }
        self.__parentByChild = {}
        self.__childrenByParent = {}

    def __mapDataType(self, oracleType):
        if not oracleType:
            return oracleType
        upper_type = oracleType.upper()
        return self.__DATA_TYPE_MAP.get(upper_type, upper_type)

    def __buildInheritanceMaps(self):
        self.__parentByChild.clear()
        self.__childrenByParent.clear()

        for inheritance in self.__InheritancesModel.getInheritances():
            child_table = inheritance.getFirstTable()
            parent_table = inheritance.getSecondTable()

            self.__parentByChild[child_table] = parent_table
            if parent_table not in self.__childrenByParent:
                self.__childrenByParent[parent_table] = []
            self.__childrenByParent[parent_table].append(child_table)

    @override
    def generateSQLCode(self):
        sqlStatements = []

        self.__buildInheritanceMaps()

        tablesWithInheritance = set(self.__parentByChild.keys()) | set(self.__childrenByParent.keys())

        for table in self.__TablesModel.getTables():
            if table not in tablesWithInheritance:
                sqlStatements.append(self._generateCreateTableSQLCode(table))

        for parentTable in self.__childrenByParent.keys():
            sqlStatements.append(self._generateCreateTableFromTypeSQLCode(parentTable))

        for childTable, parentTable in self.__parentByChild.items():
            sqlStatements.append(self._generateCreateTableFromTypeSQLCode(childTable))

        for ObtainedRelationship in self.__RelationshipsModel.getRelationships():
            sqlStatements.append(self._generateRelationshipSQLCode(ObtainedRelationship))

        return '\n\n'.join(sqlStatements)

    @override
    def _generateCreateTableSQLCode(self, ObtainedTable):
        tableName = ObtainedTable.getTableName()
        columnsSQL = []
        pkColumns = []

        tableColumns = ObtainedTable.getTableColumns()
        for column in tableColumns:
            pgType = self.__mapDataType(column["dataType"])
            columnSQL = f'"{column["columnName"]}" {pgType}'
            if column["length"]:
                columnSQL += f'({column["length"]})'
            if column["notNull"]:
                columnSQL += " NOT NULL"
            if column["unique"]:
                columnSQL += " UNIQUE"
            columnsSQL.append(columnSQL)

            if column["pk"]:
                pkColumns.append(f'"{column["columnName"]}"')

        if pkColumns:
            columnsSQL.append(f'CONSTRAINT "pk_{tableName}" PRIMARY KEY ({", ".join(pkColumns)})')

        return f'CREATE TABLE "{tableName}" (\n    ' + ',\n    '.join(columnsSQL) + '\n);'

    @override
    def _generateInheritanceTypeSQLCode(self, ObtainedInheritance):
        return ""

    @override
    def _generateCreateTableFromTypeSQLCode(self, ObtainedTable):
        tableName = ObtainedTable.getTableName()

        parentTable = self.__parentByChild.get(ObtainedTable)
        if not parentTable:
            return self._generateCreateTableSQLCode(ObtainedTable)

        parentColumns = parentTable.getTableColumns()
        childColumns = ObtainedTable.getTableColumns()

        parentColumnsByName = {c["columnName"]: c for c in parentColumns}
        childColumnsByName = {c["columnName"]: c for c in childColumns}

        mergedColumnsOrder = []
        for col in parentColumns:
            mergedColumnsOrder.append(col["columnName"])
        for col in childColumns:
            if col["columnName"] not in parentColumnsByName:
                mergedColumnsOrder.append(col["columnName"])

        mergedColumns = {}
        mergedColumns.update(parentColumnsByName)
        mergedColumns.update(childColumnsByName)

        columnsSQL = []
        pkColumns = []

        for colName in mergedColumnsOrder:
            column = mergedColumns[colName]
            pgType = self.__mapDataType(column["dataType"])
            columnSQL = f'"{column["columnName"]}" {pgType}'
            if column["length"]:
                columnSQL += f'({column["length"]})'
            if column.get("notNull"):
                columnSQL += " NOT NULL"
            if column.get("unique"):
                columnSQL += " UNIQUE"
            columnsSQL.append(columnSQL)

            if column.get("pk"):
                pkColumns.append(f'"{column["columnName"]}"')

        if not pkColumns:
            for col in parentColumns:
                if col.get("pk"):
                    pkColumns.append(f'"{col["columnName"]}"')

        if pkColumns:
            columnsSQL.append(f'CONSTRAINT "pk_{tableName}" PRIMARY KEY ({", ".join(pkColumns)})')

        if pkColumns:
            pk_col_names = [c.strip('"') for c in pkColumns]
            fk_cols_child = ", ".join(f'"{n}"' for n in pk_col_names)
            fk_cols_parent = ", ".join(f'"{n}"' for n in pk_col_names)

            parentTableName = parentTable.getTableName()
            columnsSQL.append(
                f'CONSTRAINT "fk_{tableName}_{parentTableName}" FOREIGN KEY ({fk_cols_child}) '
                f'REFERENCES "{parentTableName}"({fk_cols_parent})'
            )

        return f'CREATE TABLE "{tableName}" (\n    ' + ',\n    '.join(columnsSQL) + '\n);'

    @override
    def _generateObjectColumns(self, obtainedColumns):
        columnsSQL = []
        for column in obtainedColumns:
            pgType = self.__mapDataType(column["dataType"])
            columnSQL = f'"{column["columnName"]}" {pgType}'
            if column["length"]:
                columnSQL += f'({column["length"]})'
            columnsSQL.append(columnSQL)
        return columnsSQL

    @override
    def _generateRelationshipSQLCode(self, ObtainedRelationship):
        relationshipType = ObtainedRelationship.getRelationshipType()

        if relationshipType is RelationshipsEnum.REL_n_n:
            return self._generateCreateJunctionTableSQLCode(ObtainedRelationship)
        else:
            firstTableName = ObtainedRelationship.getFirstTable().getTableName()
            secondTableName = ObtainedRelationship.getSecondTable().getTableName()
            firstSelectedColumnName = ObtainedRelationship.getFirstSelectedColumnName()
            secondSelectedColumnName = ObtainedRelationship.getSecondSelectedColumnName()

            alterTableSQL = (
                f'ALTER TABLE "{secondTableName}" '
                f'ADD CONSTRAINT "fk_{secondTableName}_{secondSelectedColumnName}" '
                f'FOREIGN KEY ("{secondSelectedColumnName}") '
                f'REFERENCES "{firstTableName}"("{firstSelectedColumnName}");'
            )
            return alterTableSQL

    @override
    def _generateCreateJunctionTableSQLCode(self, ObtainedRelationship):
        firstTableName = ObtainedRelationship.getFirstTable().getTableName()
        secondTableName = ObtainedRelationship.getSecondTable().getTableName()

        junctionTableName = f"{firstTableName}_{secondTableName}"

        firstSelectedColumnName = ObtainedRelationship.getFirstSelectedColumnName()
        secondSelectedColumnName = ObtainedRelationship.getSecondSelectedColumnName()

        createJunctionTableSQL = (
            f'CREATE TABLE "{junctionTableName}" (\n'
            f'    "{firstTableName}_{firstSelectedColumnName}" INTEGER NOT NULL,\n'
            f'    "{secondTableName}_{secondSelectedColumnName}" INTEGER NOT NULL,\n'
            f'    CONSTRAINT "pk_{junctionTableName}" PRIMARY KEY '
            f'("{firstTableName}_{firstSelectedColumnName}","{secondTableName}_{secondSelectedColumnName}"),\n'
            f'    CONSTRAINT "fk_{junctionTableName}_{firstTableName}" FOREIGN KEY '
            f'("{firstTableName}_{firstSelectedColumnName}") REFERENCES '
            f'"{firstTableName}"("{firstSelectedColumnName}"),\n'
            f'    CONSTRAINT "fk_{junctionTableName}_{secondTableName}" FOREIGN KEY '
            f'("{secondTableName}_{secondSelectedColumnName}") REFERENCES '
            f'"{secondTableName}"("{secondSelectedColumnName}")\n'
            f');'
        )

        return createJunctionTableSQL
