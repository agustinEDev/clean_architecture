from abc import ABC, abstractmethod
from typing import List, Optional
from entities.users import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get(self, dni: str) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, dni: str) -> None:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass