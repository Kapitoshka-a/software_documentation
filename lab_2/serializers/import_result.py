from pydantic import BaseModel


class ImportResult(BaseModel):
    users: int
    clients: int
    operators: int
    conversations: int
    messages: int
    attachments: int
