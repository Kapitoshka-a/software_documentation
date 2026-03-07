from datetime import datetime, timezone
from uuid import UUID

from core.interfaces import OperatorRepositoryInterface, ConversationRepositoryInterface
from db_models import Operator, Conversation


class OperatorController:
    def __init__(
        self,
        operator_repository: OperatorRepositoryInterface,
        conversation_repository: ConversationRepositoryInterface,
    ) -> None:
        self._operator_repository = operator_repository
        self._conversation_repository = conversation_repository

    def get_details(self, operator_id: UUID) -> Operator:
        operator = self._operator_repository.get(operator_id)
        if operator is None:
            raise ValueError("Operator not found")
        return operator

    def assign_conversation(self, conversation_id: UUID, operator_id: UUID) -> Conversation:
        conversation = self._conversation_repository.get(conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        conversation.operator_id = operator_id
        return self._conversation_repository.update(conversation)

    def transfer_conversation(self, conversation_id: UUID, target_operator_id: UUID) -> Conversation:
        return self.assign_conversation(conversation_id, target_operator_id)

    def resolve_conversation(self, conversation_id: UUID, closed_at: datetime | None = None) -> Conversation:
        conversation = self._conversation_repository.get(conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        conversation.status = "closed"
        conversation.closed_at = closed_at or datetime.now(timezone.utc)
        return self._conversation_repository.update(conversation)
