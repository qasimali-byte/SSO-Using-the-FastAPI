from abc import ABC, abstractmethod

class UserRole(ABC):

    @abstractmethod
    def get_user_role(self):
        raise NotImplementedError()

class UserEmail(ABC):
    
    @abstractmethod
    def get_user_email(self):
        raise NotImplementedError()

class RoleVerifier(ABC):

    @abstractmethod
    def verify(self):
        raise NotImplementedError()