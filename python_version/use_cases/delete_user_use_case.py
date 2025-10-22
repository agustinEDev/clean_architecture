import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from typing import Optional
from use_cases.user_repository_interface import UserRepositoryInterface
from entities.users import User

class DeleteUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, dni: str) -> None:
        user = self.repository.get(dni)
        if not user:
            raise ValueError(f"Usuario con DNI {dni} no encontrado para eliminar")
        self.repository.delete(dni)