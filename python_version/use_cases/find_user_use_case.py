from entities.users import User
from use_cases.user_repository_interface import UserRepositoryInterface

class FindUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, dni: str) -> User:
        user = self.repository.get(dni)
        if not user:
            raise ValueError(f"Usuario con DNI {dni} no encontrado")
        return user