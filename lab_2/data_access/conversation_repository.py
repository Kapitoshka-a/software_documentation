from sqlmodel import Session, select

from core.errors import EntityNotFoundError, EntityAlreadyExistsError
from core.interfaces import ConversationRepositoryInterface
from db_models import Conversation


class ConversationRepository(ConversationRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, conversation: Conversation) -> Conversation:
        existing = self._session.get(Conversation, conversation.id)
        if existing:
            raise EntityAlreadyExistsError("Conversation", f"id={conversation.id}")
        self._session.add(conversation)
        self._session.commit()
        self._session.refresh(conversation)
        return conversation

    def get(
        self,
        conversation_id: str | None = None,
        operator_id: str | None = None,
        client_id: str | None = None,
        is_unassigned: bool = False,
        offset: int = 1,
        limit: int = 100
    ) -> Conversation | list[Conversation]:
        statement = select(Conversation).where(*(
            Conversation.id == conversation_id if conversation_id else True,
            Conversation.operator_id == operator_id if operator_id else True,
            Conversation.client_id == client_id if client_id else True,
            Conversation.operator_id.is_(None) if is_unassigned else True
        ))
        if conversation_id:
            conversation = self._session.exec(statement).first()
            return conversation

        statement = statement.offset((offset - 1) * limit).limit(limit)
        return list(self._session.exec(statement).all())

    def update(self, conversation: Conversation) -> Conversation:
        existing = self._session.get(Conversation, conversation.id)
        if existing is None:
            raise EntityNotFoundError("Conversation", conversation.id)
        merged = self._session.merge(conversation)
        self._session.commit()
        self._session.refresh(merged)
        return merged

    def delete(self, conversation_id: str) -> None:
        conversation = self._session.get(Conversation, conversation_id)
        if conversation is None:
            raise EntityNotFoundError("Conversation", conversation_id)
        self._session.delete(conversation)
        self._session.commit()
