from abc import ABC, abstractmethod


class ConnectionParamsDialogController(ABC):
    def __init__(self, ConnectionsParamsDialogView):
        self._ConnectionsParamsView = ConnectionsParamsDialogView
        self._ConnectionsParamsView.cancelButton.clicked.connect(self.__selectCancel)
        self._ConnectionsParamsView.okButton.clicked.connect(self.__selectOK)

    def __selectCancel(self):
        self._ConnectionsParamsView.reject()

    def __selectOK(self):
        if self._editConnectionParams():
            self._ConnectionsParamsView.accept()

    @abstractmethod
    def _editConnectionParams(self):
        pass

    @abstractmethod
    def getConnectionParams(self):
        pass
