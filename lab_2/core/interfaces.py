from __future__ import annotations
from typing import Generic, TypeVar
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


class ReadCreateRepositoryInterface(ABC, Generic[T, ID]):
    @abstractmethod
    def create(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get(self, entity_id: ID | None = None, offset: int = 1, limit: int = 100) -> T | list[T]:
        raise NotImplementedError


class UserRepositoryInterface(CrudRepositoryInterface[User, str]):
    @abstractmethod
    def get(self, user_id: ID | None = None, name: str | None = None, offset: int = 1, limit: int = 100) -> T | list[T]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, operator_id):
        raise NotImplementedError


class ClientRepositoryInterface(CrudRepositoryInterface[Client, str]):
    pass


class OperatorRepositoryInterface(CrudRepositoryInterface[Operator, str]):
    pass


class ConversationRepositoryInterface(CrudRepositoryInterface[Conversation, str]):
    def get(self, conversation_id: str | None = None, operator_id: str | None = None, client_id: str | None = None):
        raise NotImplementedError


class MessageRepositoryInterface(ReadCreateRepositoryInterface[Message, str]):
    pass


class AttachmentRepositoryInterface(CrudRepositoryInterface[Attachment, str]):
    @abstractmethod
    def list_by_message(self, message_id: str) -> list[Attachment]:
        raise NotImplementedError

