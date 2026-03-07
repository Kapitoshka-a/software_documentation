from datetime import datetime, timezone
from uuid import UUID, uuid4

from core.interfaces import MessageRepositoryInterface
from db_models import Message


class MessageController:
    def __init__(self, message_repository: MessageRepositoryInterface) -> None:
        self._message_repository = message_repository

    def create_message(
        self,
        conversation_id: UUID,
        content: str,
        timestamp: datetime | None = None,
        is_read: bool = False,
    ) -> Message:
        message = Message(
            id=uuid4(),
            content=content,
            timestamp=timestamp or datetime.now(timezone.utc),
            is_read=is_read,
            conversation_id=conversation_id,
        )
        return self._message_repository.create(message)

    def get_message(self, message_id: UUID) -> Message:
        message = self._message_repository.get(message_id)
        if message is None:
            raise ValueError("Message not found")
        return message

    def list_messages(self, conversation_id: UUID) -> list[Message]:
        return self._message_repository.list_by_conversation(conversation_id)
