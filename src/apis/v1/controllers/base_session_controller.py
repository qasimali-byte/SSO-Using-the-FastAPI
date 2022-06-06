from abc import ABC, abstractmethod

class Store(ABC):
    """Abstract class that defines methods for interacting with session data. """

    @abstractmethod
    def get(self, filter_key: str, filter_value: str) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def set(self, cookieid, userid):
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, filter_key: str, filter_value: str):
        raise NotImplementedError()

 