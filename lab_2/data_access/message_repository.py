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

    def get(
            self,
            message_id: str | None = None,
            conversation_id: str | None = None,
            sender_role: str | None = None,
            offset: int = 1,
            limit: int = 100
    ) -> Message | list[Message]:
        statement = select(Message).where(*(
            Message.id == message_id if message_id else True,
            Message.conversation_id == conversation_id if conversation_id else True,
            Message.sender_role == sender_role if sender_role else True
        ))
        if message_id:
            return  self._session.exec(statement).first()

        statement = statement.offset((offset - 1) * limit).limit(limit)
        return list(self._session.exec(statement).all())

