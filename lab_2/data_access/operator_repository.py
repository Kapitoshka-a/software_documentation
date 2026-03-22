from sqlmodel import Session, select

from core.errors import EntityNotFoundError, EntityAlreadyExistsError
from core.interfaces import OperatorRepositoryInterface
from db_models import Operator


class OperatorRepository(OperatorRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, operator: Operator) -> Operator:
        existing = self._session.get(Operator, operator.id)
        if existing:
            raise EntityAlreadyExistsError("Operator", f"id={operator.id}")
        self._session.add(operator)
        self._session.commit()
        self._session.refresh(operator)
        return operator

    def get(self, operator_id: str | None = None, offset: int = 1, limit: int = 100) -> Operator | list[Operator]:
        statement = select(Operator)
        if operator_id:
            statement = statement.where(Operator.id == operator_id)
            return self._session.exec(statement).first()
        statement = statement.offset((offset - 1) * limit).limit(limit)
        return list(self._session.exec(statement).all())

    def update(self, operator: Operator) -> Operator:
        existing = self._session.get(Operator, operator.id)
        if existing is None:
            raise EntityNotFoundError("Operator", operator.id)
        merged = self._session.merge(operator)
        self._session.commit()
        self._session.refresh(merged)
        return merged
