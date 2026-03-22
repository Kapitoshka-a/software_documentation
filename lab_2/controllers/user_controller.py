from uuid import UUID

from core.interfaces import UserRepositoryInterface
from db_models import User


class UserController:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    def get_details(self, user_id: UUID) -> User:
        user = self._user_repository.get(user_id)
        if user is None:
            raise ValueError("User not found")
        return user

    def update_contact_info(self, user_id: UUID, name: str, email: str) -> User:
        user = self._user_repository.get(user_id)
        if user is None:
            raise ValueError("User not found")
        user.name = name
        user.email = email
        return self._user_repository.update(user)
