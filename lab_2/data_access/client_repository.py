from uuid import UUID

from sqlmodel import Session, select

from core.errors import EntityNotFoundError, EntityAlreadyExistsError
from core.interfaces import ClientRepositoryInterface
from db_models import Client


class ClientRepository(ClientRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, client: Client) -> Client:
        existing = self._session.get(Client, client.id)
        if existing:
            raise EntityAlreadyExistsError("Client", f"id={client.id}")
        self._session.add(client)
        self._session.commit()
        self._session.refresh(client)
        return client

    def get(self, client_id: UUID | None = None, offset: int = 1, limit: int = 100) -> Client | list[Client]:
        statement = select(Client)
        if client_id:
            statement = statement.where(Client.id == client_id)
            client = self._session.exec(statement).first()
            if not client:
                raise EntityNotFoundError("Client", client_id)
            return client
        statement = statement.offset((offset - 1) * limit).limit(limit)
        return list(self._session.exec(statement).all())

    def update(self, client: Client) -> Client:
        existing = self._session.get(Client, client.id)
        if existing is None:
            raise EntityNotFoundError("Client", client.id)
        merged = self._session.merge(client)
        self._session.commit()
        self._session.refresh(merged)
        return merged

    def delete(self, client_id: UUID) -> None:
        client = self._session.get(Client, client_id)
        if client is None:
            raise EntityNotFoundError("Client", client_id)
        self._session.delete(client)
        self._session.commit()
