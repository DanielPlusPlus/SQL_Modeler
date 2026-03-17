from abc import ABC, abstractmethod


class DatabaseControllerInterface(ABC):
    @abstractmethod
    def executeSQLCode(self, sqlCode):
        pass
