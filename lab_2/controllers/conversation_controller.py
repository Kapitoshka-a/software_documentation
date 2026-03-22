from datetime import datetime, timezone
from uuid import uuid4

from core.interfaces import ConversationRepositoryInterface, MessageRepositoryInterface
from db_models import Conversation, Message


class ConversationController:
    def __init__(
        self,
        conversation_repository: ConversationRepositoryInterface,
        message_repository: MessageRepositoryInterface,
    ) -> None:
        self._conversation_repository = conversation_repository
        self._message_repository = message_repository

    def add_message(
        self,
        conversation_id: str,
        content: str,
        sender_role: str,
        timestamp: datetime | None = None,
        is_read: bool = False,
    ) -> Message:
        if self._conversation_repository.get(conversation_id) is None:
            raise ValueError("Conversation not found")
        message = Message(
            id=str(uuid4()),
            content=content,
            timestamp=timestamp or datetime.now(timezone.utc),
            is_read=is_read,
            conversation_id=conversation_id,
            sender_role=sender_role,
        )
        return self._message_repository.create(message)

    def change_status(self, conversation_id: str, new_status: str) -> Conversation:
        conversation = self._conversation_repository.get(conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        conversation.status = new_status
        return self._conversation_repository.update(conversation)

    def assign_to(self, conversation_id: str, operator_id: str) -> Conversation:
        conversation = self._conversation_repository.get(conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        conversation.operator_id = operator_id
        return self._conversation_repository.update(conversation)

    def get(self, **kwargs) -> Conversation:
        return self._conversation_repository.get(**kwargs)
