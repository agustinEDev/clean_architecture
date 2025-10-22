import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from typing import Optional
from use_cases.user_repository_interface import UserRepositoryInterface
from entities.users import User

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, dni: str, new_username: str, new_last_name: str) -> Optional[User]:
        updated_user = self.user_repository.update(dni, new_username, new_last_name)
        if not updated_user:
            raise ValueError(f"Usuario con DNI {dni} no encontrado para actualizar")
        return updated_user