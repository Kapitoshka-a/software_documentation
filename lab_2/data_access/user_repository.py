from uuid import UUID

from sqlmodel import Session, select

from core.errors import EntityNotFoundError, UserEmailAlreadyExistsError
from core.interfaces import UserRepositoryInterface
from db_models import User


class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: User) -> User:
        existing = self._session.exec(select(User).where(User.email == user.email)).first()
        if existing:
            raise UserEmailAlreadyExistsError(user.email)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get(self, user_id: UUID | None = None, offset: int = 1, limit: int = 100) -> User | list[User]:
        statement = select(User)
        if user_id:
            statement = statement.where(User.id == user_id)
            user = self._session.exec(statement).first()
            if not user:
                raise EntityNotFoundError("User", user_id)
            return user
        statement = statement.offset((offset - 1) * limit).limit(limit)
        return list(self._session.exec(statement).all())

    def update(self, user: User) -> User:
        existing = self._session.get(User, user.id)
        if existing is None:
            raise EntityNotFoundError("User", user.id)
        duplicate = self._session.exec(
            select(User).where(User.email == user.email, User.id != user.id)
        ).first()
        if duplicate:
            raise UserEmailAlreadyExistsError(user.email)
        merged = self._session.merge(user)
        self._session.commit()
        self._session.refresh(merged)
        return merged

    def delete(self, user_id: UUID) -> None:
        user = self._session.get(User, user_id)
        if user is None:
            raise EntityNotFoundError("User", user_id)
        self._session.delete(user)
        self._session.commit()
