from datetime import datetime, timezone
from uuid import uuid4

from core.interfaces import ClientRepositoryInterface, ConversationRepositoryInterface, MessageRepositoryInterface, \
    UserRepositoryInterface
from db_models import Client, Conversation, Message


class ClientController:
    def __init__(
        self,
        client_repository: ClientRepositoryInterface,
        conversation_repository: ConversationRepositoryInterface,
        message_repository: MessageRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> None:
        self._client_repository = client_repository
        self._conversation_repository = conversation_repository
        self._message_repository = message_repository
        self._user_repository = user_repository

    def get_details(self, client_id: str) -> Client | None:
        exist = self._user_repository.get(user_id=client_id)
        if not exist:
            return None

        return self._client_repository.get(client_id=client_id)

    def initiate_conversation(
        self,
        client_id: str,
        priority: str,
        status: str = "open",
        operator_id: str | None = None,
    ) -> Conversation:
        if self._client_repository.get(client_id) is None:
            raise ValueError("Client not found")
        conversation = Conversation(
            id=str(uuid4()),
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
        client_id: str,
        conversation_id: str,
        content: str,
        sender_role: str = "client",
    ) -> Message:
        if self._client_repository.get(client_id) is None:
            raise ValueError("Client not found")
        message = Message(
            id=str(uuid4()),
            content=content,
            timestamp=datetime.now(timezone.utc),
            is_read=False,
            conversation_id=conversation_id,
            sender_role=sender_role,
        )
        return self._message_repository.create(message)

    def delete_client(self, client_id: str) -> None:
        self._user_repository.delete(client_id)
