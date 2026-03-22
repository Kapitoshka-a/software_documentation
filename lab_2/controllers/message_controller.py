from datetime import datetime, timezone
from uuid import uuid4

from core.interfaces import MessageRepositoryInterface
from db_models import Message


class MessageController:
    def __init__(self, message_repository: MessageRepositoryInterface) -> None:
        self._message_repository = message_repository

    def create_message(
        self,
        conversation_id: str,
        content: str,
        sender_role: str,
        timestamp: datetime | None = None,
        is_read: bool = False,
    ) -> Message:
        message = Message(
            id=str(uuid4()),
            content=content,
            timestamp=timestamp or datetime.now(timezone.utc),
            is_read=is_read,
            conversation_id=conversation_id,
            sender_role=sender_role,
        )
        return self._message_repository.create(message)

    def get_messages(self, **kwargs) -> Message | list[Message]:
        return self._message_repository.get(**kwargs)
