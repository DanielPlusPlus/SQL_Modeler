from abc import ABC, abstractmethod


class LoadSQLControllerInterface(ABC):
    @abstractmethod
    def parseSQLCode(self, sqlCode):
        pass
