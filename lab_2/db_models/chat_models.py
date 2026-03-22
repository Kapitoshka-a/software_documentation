from datetime import datetime
from uuid import uuid4

from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=uuid4, primary_key=True)
    status: str
    priority: str
    started_at: datetime
    closed_at: datetime | None = None

    client_id: str = Field(foreign_key="clients.id")
    operator_id: str | None = Field(foreign_key="operators.id", nullable=True)

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=uuid4, primary_key=True)
    content: str
    timestamp: datetime
    is_read: bool
    sender_role: str

    conversation_id: str = Field(foreign_key="conversations.id")

class Attachment(SQLModel, table=True):
    __tablename__ = "attachments"

    id: str = Field(default_factory=uuid4, primary_key=True)
    file_name: str
    file_size: int
    file_type: str

    message_id: str = Field(foreign_key="messages.id")
