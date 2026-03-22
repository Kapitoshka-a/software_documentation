from datetime import datetime
from typing import Mapping
from uuid import UUID

from serializers.import_bundle import ImportBundle
from core.interfaces import CsvDataSourceInterface, RepositoryInterface
from db_models import User, Client, Operator, Conversation, Message, Attachment
from serializers.import_result import ImportResult


class ImportController:
    def __init__(self, csv_source: CsvDataSourceInterface, repository: RepositoryInterface) -> None:
        self._csv_source = csv_source
        self._repository = repository

    def import_from_csv(self, file_path: str) -> ImportResult:
        rows = self._csv_source.read_rows(file_path)
        bundle = self._build_bundle(rows)
        self._repository.save_bundle(bundle)
        return ImportResult(
            users=len(bundle.users),
            clients=len(bundle.clients),
            operators=len(bundle.operators),
            conversations=len(bundle.conversations),
            messages=len(bundle.messages),
            attachments=len(bundle.attachments),
        )

    def _build_bundle(self, rows: list[Mapping[str, str]]) -> ImportBundle:
        users: dict[UUID, User] = {}
        clients: dict[UUID, Client] = {}
        operators: dict[UUID, Operator] = {}
        conversations: dict[UUID, Conversation] = {}
        messages: dict[UUID, Message] = {}
        attachments: dict[UUID, Attachment] = {}

        for row in rows:
            client_user_id = UUID(row["client_user_id"])
            if client_user_id not in users:
                users[client_user_id] = User(
                    id=client_user_id,
                    name=row["client_name"],
                    email=row["client_email"],
                    created_at=_parse_datetime(row["client_created_at"]),
                )
            if client_user_id not in clients:
                clients[client_user_id] = Client(
                    id=client_user_id,
                    company_name=row["client_company_name"],
                    hubspot_score=int(row["client_hubspot_score"]),
                    subscription_tier=row["client_subscription_tier"],
                )

            operator_user_id = UUID(row["operator_user_id"])
            if operator_user_id not in users:
                users[operator_user_id] = User(
                    id=operator_user_id,
                    name=row["operator_name"],
                    email=row["operator_email"],
                    created_at=_parse_datetime(row["operator_created_at"]),
                )
            if operator_user_id not in operators:
                operators[operator_user_id] = Operator(
                    id=operator_user_id,
                    operator_code=row["operator_code"],
                    department=row["operator_department"],
                    current_status=row["operator_current_status"],
                    max_concurrent_chats=int(row["operator_max_concurrent_chats"]),
                )

            conversation_id = UUID(row["conversation_id"])
            if conversation_id not in conversations:
                closed_at_raw = row.get("conversation_closed_at", "")
                conversations[conversation_id] = Conversation(
                    id=conversation_id,
                    status=row["conversation_status"],
                    priority=row["conversation_priority"],
                    started_at=_parse_datetime(row["conversation_started_at"]),
                    closed_at=_parse_datetime(closed_at_raw) if closed_at_raw else None,
                    client_id=client_user_id,
                    operator_id=operator_user_id,
                )

            message_id = UUID(row["message_id"])
            if message_id not in messages:
                messages[message_id] = Message(
                    id=message_id,
                    content=row["message_content"],
                    timestamp=_parse_datetime(row["message_timestamp"]),
                    is_read=_parse_bool(row["message_is_read"]),
                    conversation_id=conversation_id,
                )

            attachment_id_raw = row.get("attachment_id", "")
            if attachment_id_raw:
                attachment_id = UUID(attachment_id_raw)
                if attachment_id not in attachments:
                    attachments[attachment_id] = Attachment(
                        id=attachment_id,
                        file_name=row["attachment_file_name"],
                        file_size=int(row["attachment_file_size"]),
                        file_type=row["attachment_file_type"],
                        message_id=message_id,
                    )

        return ImportBundle(
            users=list(users.values()),
            clients=list(clients.values()),
            operators=list(operators.values()),
            conversations=list(conversations.values()),
            messages=list(messages.values()),
            attachments=list(attachments.values()),
        )


def _parse_bool(raw_value: str) -> bool:
    return raw_value.strip().lower() in {"true", "1", "yes"}


def _parse_datetime(raw_value: str) -> datetime:
    return datetime.fromisoformat(raw_value)
