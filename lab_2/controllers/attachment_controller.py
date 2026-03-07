from uuid import UUID, uuid4

from core.interfaces import AttachmentRepositoryInterface
from db_models import Attachment


class AttachmentController:
    def __init__(self, attachment_repository: AttachmentRepositoryInterface) -> None:
        self._attachment_repository = attachment_repository

    def create_attachment(
        self,
        message_id: UUID,
        file_name: str,
        file_size: int,
        file_type: str,
    ) -> Attachment:
        attachment = Attachment(
            id=uuid4(),
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            message_id=message_id,
        )
        return self._attachment_repository.create(attachment)

    def get_attachment(self, attachment_id: UUID) -> Attachment:
        attachment = self._attachment_repository.get(attachment_id)
        if attachment is None:
            raise ValueError("Attachment not found")
        return attachment

    def update_attachment(self, attachment: Attachment) -> Attachment:
        return self._attachment_repository.update(attachment)

    def list_attachments(self, message_id: UUID) -> list[Attachment]:
        return self._attachment_repository.list_by_message(message_id)
