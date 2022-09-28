from abc import ABC, abstractmethod

class DAO(ABC):

    @abstractmethod
    def get(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_all(self, filter_data):
        raise NotImplementedError()

    @abstractmethod
    def save(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()

    @abstractmethod
    def delete(self):
        raise NotImplementedError()