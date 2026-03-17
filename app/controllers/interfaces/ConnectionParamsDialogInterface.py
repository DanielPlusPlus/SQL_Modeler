from abc import ABC, abstractmethod


class ConnectionParamsDialogInterface(ABC):
    @abstractmethod
    def getConnectionParams(self):
        pass
