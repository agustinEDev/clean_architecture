from entities.users import User
from use_cases.user_repository_interface import UserRepositoryInterface

class ListUsersUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self) -> list[User]:
        return self.repository.list()