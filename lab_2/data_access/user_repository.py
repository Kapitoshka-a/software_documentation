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

    def get(
            self,
            name: str | None = None,
            user_id: str | None = None,
            offset: int = 1,
            limit: int = 100
    ) -> User | list[User]:
        statement = select(User).where(*(
            User.is_deleted == False,
            User.name == name if name else True,
            User.id == user_id if user_id else True
        ))
        if user_id or name:
            return self._session.exec(statement).first()

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

    def delete(self, user_id: str) -> None:
        user = self._session.get(User, user_id)
        if user is None:
            raise EntityNotFoundError("User", user_id)
        user.is_deleted = True
        self._session.commit()
