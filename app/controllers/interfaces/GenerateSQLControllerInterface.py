from abc import ABC, abstractmethod


class GenerateSQLControllerInterface(ABC):
    @abstractmethod
    def generateSQLCode(self):
        pass

    @abstractmethod
    def _generateCreateTableSQLCode(self, ObtainedTable):
        pass

    @abstractmethod
    def _generateInheritanceTypeSQLCode(self, ObtainedInheritance):
        pass

    @abstractmethod
    def _generateCreateTableFromTypeSQLCode(self, ObtainedTable):
        pass

    @abstractmethod
    def _generateObjectColumns(self, obtainedColumns):
        pass

    @abstractmethod
    def _generateRelationshipSQLCode(self, ObtainedRelationship):
        pass

    @abstractmethod
    def _generateCreateJunctionTableSQLCode(self, ObtainedRelationship):
        pass