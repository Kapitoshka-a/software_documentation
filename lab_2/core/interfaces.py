from __future__ import annotations
from typing import Generic, TypeVar
from uuid import UUID
from abc import ABC, abstractmethod
from typing import Mapping

from serializers.import_bundle import ImportBundle

from db_models import User, Client, Operator, Conversation, Message, Attachment


T = TypeVar("T")
ID = TypeVar("ID")


class CsvDataSourceInterface(ABC):
    @abstractmethod
    def read_rows(self, file_path: str) -> list[Mapping[str, str]]:
        raise NotImplementedError


class RepositoryInterface(ABC):
    @abstractmethod
    def save_bundle(self, bundle: ImportBundle) -> None:
        raise NotImplementedError


class CrudRepositoryInterface(ABC, Generic[T, ID]):
    @abstractmethod
    def create(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get(self, entity_id: ID | None = None, offset: int = 1, limit: int = 100) -> T | list[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        raise NotImplementedError


class ReadCreateRepositoryInterface(ABC, Generic[T, ID]):
    @abstractmethod
    def create(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get(self, entity_id: ID | None = None, offset: int = 1, limit: int = 100) -> T | list[T]:
        raise NotImplementedError


class UserRepositoryInterface(CrudRepositoryInterface[User, UUID]):
    pass


class ClientRepositoryInterface(CrudRepositoryInterface[Client, UUID]):
    pass


class OperatorRepositoryInterface(CrudRepositoryInterface[Operator, UUID]):
    pass


class ConversationRepositoryInterface(CrudRepositoryInterface[Conversation, UUID]):
    pass


class MessageRepositoryInterface(ReadCreateRepositoryInterface[Message, UUID]):
    @abstractmethod
    def list_by_conversation(self, conversation_id: UUID) -> list[Message]:
        raise NotImplementedError


class AttachmentRepositoryInterface(CrudRepositoryInterface[Attachment, UUID]):
    @abstractmethod
    def list_by_message(self, message_id: UUID) -> list[Attachment]:
        raise NotImplementedError

