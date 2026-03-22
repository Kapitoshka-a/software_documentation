from dataclasses import dataclass
from typing import List

from db_models import User, Client, Operator, Conversation, Message, Attachment


@dataclass(frozen=True)
class ImportBundle:
    users: List[User]
    clients: List[Client]
    operators: List[Operator]
    conversations: List[Conversation]
    messages: List[Message]
    attachments: List[Attachment]
