from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: str
    created_at: datetime

class Client(SQLModel, table=True):
    __tablename__ = "clients"

    id: UUID = Field(foreign_key="users.id", primary_key=True)
    company_name: str
    hubspot_score: int
    subscription_tier: str

class Operator(SQLModel, table=True):
    __tablename__ = "operators"

    id: UUID = Field(foreign_key="users.id", primary_key=True)
    operator_code: str
    department: str
    current_status: str
    max_concurrent_chats: int
