from entities.users import User
from use_cases.user_repository_interface import UserRepositoryInterface

class CreateUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, username: str, lastname: str, dni: str):
        # Create user instance
        user = User(username, lastname, dni)
        # Save user using the repository
        return self.repository.save(user)