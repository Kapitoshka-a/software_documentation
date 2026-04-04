from sqlmodel import Session, select

from core.errors import EntityNotFoundError, EntityAlreadyExistsError
from core.interfaces import AttachmentRepositoryInterface
from db_models import Attachment


class AttachmentRepository(AttachmentRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, attachment: Attachment) -> Attachment:
        existing = self._session.get(Attachment, attachment.id)
        if existing:
            raise EntityAlreadyExistsError("Attachment", f"id={attachment.id}")
        self._session.add(attachment)
        self._session.commit()
        self._session.refresh(attachment)
        return attachment

    def get(
        self, attachment_id: str | None = None, offset: int = 1, limit: int = 100
    ) -> Attachment | list[Attachment]:
        statement = select(Attachment)
        if attachment_id:
            statement = statement.where(Attachment.id == attachment_id)
            attachment = self._session.exec(statement).first()
            if not attachment:
                raise EntityNotFoundError("Attachment", attachment_id)
            return attachment
        statement = statement.offset((offset - 1) * limit).limit(limit)
        return list(self._session.exec(statement).all())

    def update(self, attachment: Attachment) -> Attachment:
        existing = self._session.get(Attachment, attachment.id)
        if existing is None:
            raise EntityNotFoundError("Attachment", attachment.id)
        merged = self._session.merge(attachment)
        self._session.commit()
        self._session.refresh(merged)
        return merged

    def delete(self, attachment_id: str) -> None:
        attachment = self._session.get(Attachment, attachment_id)
        if attachment is None:
            raise EntityNotFoundError("Attachment", attachment_id)
        self._session.delete(attachment)
        self._session.commit()

    def list_by_message(self, message_id: str) -> list[Attachment]:
        statement = select(Attachment).where(Attachment.message_id == message_id)
        return list(self._session.exec(statement).all())
