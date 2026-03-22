from uuid import UUID

from sqlmodel import Session, select

from core.errors import EntityNotFoundError, EntityAlreadyExistsError
from core.interfaces import MessageRepositoryInterface
from db_models import Message


class MessageRepository(MessageRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, message: Message) -> Message:
        existing = self._session.get(Message, message.id)
        if existing:
            raise EntityAlreadyExistsError("Message", f"id={message.id}")
        self._session.add(message)
        self._session.commit()
        self._session.refresh(message)
        return message

    def get(self, message_id: UUID | None = None, offset: int = 1, limit: int = 100) -> Message | list[Message]:
        statement = select(Message)
        if message_id:
            statement = statement.where(Message.id == message_id)
            message = self._session.exec(statement).first()
            if not message:
                raise EntityNotFoundError("Message", message_id)
            return message
        statement = statement.offset((offset - 1) * limit).limit(limit)
        return list(self._session.exec(statement).all())

    def list_by_conversation(self, conversation_id: UUID) -> list[Message]:
        statement = select(Message).where(Message.conversation_id == conversation_id)
        return list(self._session.exec(statement).all())
