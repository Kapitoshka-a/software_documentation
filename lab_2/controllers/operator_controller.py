from datetime import datetime, timezone

from core.interfaces import OperatorRepositoryInterface, ConversationRepositoryInterface, UserRepositoryInterface
from db_models import Operator, Conversation


class OperatorController:
    def __init__(
        self,
        operator_repository: OperatorRepositoryInterface,
        conversation_repository: ConversationRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> None:
        self._operator_repository = operator_repository
        self._conversation_repository = conversation_repository
        self._user_repository = user_repository

    def get_details(self, operator_id: str) -> Operator | None:
        exist = self._user_repository.get(user_id=operator_id)
        if not exist:
            print("User not found")
            return None

        return self._operator_repository.get(operator_id)

    def assign_conversation(self, conversation_id: str, operator_id: str) -> Conversation:
        conversation = self._conversation_repository.get(conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        conversation.operator_id = operator_id
        return self._conversation_repository.update(conversation)

    def transfer_conversation(self, conversation_id: str, target_operator_id: str) -> Conversation:
        return self.assign_conversation(conversation_id, target_operator_id)

    def resolve_conversation(self, conversation_id: str, closed_at: datetime | None = None) -> Conversation:
        conversation = self._conversation_repository.get(conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        conversation.status = "closed"
        conversation.closed_at = closed_at or datetime.now(timezone.utc)
        return self._conversation_repository.update(conversation)

    def delete_operator(self, operator_id: str) -> None:
        self._user_repository.delete(operator_id)
