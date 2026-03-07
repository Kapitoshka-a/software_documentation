from datetime import datetime, timezone
from uuid import UUID, uuid4

from core.interfaces import ClientRepositoryInterface, ConversationRepositoryInterface, MessageRepositoryInterface
from db_models import Client, Conversation, Message


class ClientController:
    def __init__(
        self,
        client_repository: ClientRepositoryInterface,
        conversation_repository: ConversationRepositoryInterface,
        message_repository: MessageRepositoryInterface,
    ) -> None:
        self._client_repository = client_repository
        self._conversation_repository = conversation_repository
        self._message_repository = message_repository

    def get_details(self, client_id: UUID) -> Client:
        client = self._client_repository.get(client_id)
        if client is None:
            raise ValueError("Client not found")
        return client

    def initiate_conversation(
        self,
        client_id: UUID,
        operator_id: UUID,
        priority: str,
        status: str = "open",
    ) -> Conversation:
        if self._client_repository.get(client_id) is None:
            raise ValueError("Client not found")
        conversation = Conversation(
            id=uuid4(),
            status=status,
            priority=priority,
            started_at=datetime.now(timezone.utc),
            closed_at=None,
            client_id=client_id,
            operator_id=operator_id,
        )
        return self._conversation_repository.create(conversation)

    def submit_feedback(
        self,
        client_id: UUID,
        conversation_id: UUID,
        content: str,
    ) -> Message:
        if self._client_repository.get(client_id) is None:
            raise ValueError("Client not found")
        message = Message(
            id=uuid4(),
            content=content,
            timestamp=datetime.now(timezone.utc),
            is_read=False,
            conversation_id=conversation_id,
        )
        return self._message_repository.create(message)
