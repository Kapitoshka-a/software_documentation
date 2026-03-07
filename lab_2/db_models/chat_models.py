from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: str
    priority: str
    started_at: datetime
    closed_at: datetime | None = None

    client_id: UUID = Field(foreign_key="clients.id")
    operator_id: UUID = Field(foreign_key="operators.id")

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    content: str
    timestamp: datetime
    is_read: bool

    conversation_id: UUID = Field(foreign_key="conversations.id")

class Attachment(SQLModel, table=True):
    __tablename__ = "attachments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    file_name: str
    file_size: int
    file_type: str

    message_id: UUID = Field(foreign_key="messages.id")
