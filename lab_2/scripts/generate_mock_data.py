import argparse
import csv
import os
import random
from datetime import datetime, timedelta, timezone
from uuid import uuid4


CLIENT_TIERS = ["free", "standard", "premium", "enterprise"]
DEPARTMENTS = ["support", "sales", "billing", "tech"]
STATUSES = ["online", "offline", "busy", "away"]
PRIORITIES = ["low", "medium", "high"]
CONVERSATION_STATUSES = ["open", "pending", "closed"]
FILE_TYPES = ["png", "jpg", "pdf", "txt"]


def _random_email(name: str, idx: int) -> str:
    return f"{name.lower()}.{idx}@example.com"


def _random_name(prefix: str, idx: int) -> str:
    return f"{prefix} {idx}"


def _random_company(idx: int) -> str:
    return f"Company {idx}"


def _random_sentence(idx: int) -> str:
    return f"Message content {idx}"


def generate_csv(path: str, rows: int) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    random.seed(42)

    client_count = max(50, rows // 20)
    operator_count = max(10, rows // 200)
    conversation_count = max(100, rows // 10)

    clients = []
    for idx in range(client_count):
        user_id = uuid4()
        created_at = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 365))
        clients.append(
            {
                "client_user_id": str(user_id),
                "client_name": _random_name("Client", idx + 1),
                "client_email": _random_email("client", idx + 1),
                "client_created_at": created_at.isoformat(),
                "client_company_name": _random_company(idx + 1),
                "client_hubspot_score": str(random.randint(1, 100)),
                "client_subscription_tier": random.choice(CLIENT_TIERS),
            }
        )

    operators = []
    for idx in range(operator_count):
        user_id = uuid4()
        created_at = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 365))
        operators.append(
            {
                "operator_user_id": str(user_id),
                "operator_name": _random_name("Operator", idx + 1),
                "operator_email": _random_email("operator", idx + 1),
                "operator_created_at": created_at.isoformat(),
                "operator_code": f"OP-{idx + 1:04d}",
                "operator_department": random.choice(DEPARTMENTS),
                "operator_current_status": random.choice(STATUSES),
                "operator_max_concurrent_chats": str(random.randint(2, 8)),
            }
        )

    conversations = []
    for idx in range(conversation_count):
        client = random.choice(clients)
        operator = random.choice(operators)
        started_at = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))
        status = random.choice(CONVERSATION_STATUSES)
        closed_at = ""
        if status == "closed":
            closed_at = (started_at + timedelta(hours=random.randint(1, 48))).isoformat()
        conversations.append(
            {
                "conversation_id": str(uuid4()),
                "conversation_status": status,
                "conversation_priority": random.choice(PRIORITIES),
                "conversation_started_at": started_at.isoformat(),
                "conversation_closed_at": closed_at,
                "client": client,
                "operator": operator,
            }
        )

    fieldnames = [
        "client_user_id",
        "client_name",
        "client_email",
        "client_created_at",
        "client_company_name",
        "client_hubspot_score",
        "client_subscription_tier",
        "operator_user_id",
        "operator_name",
        "operator_email",
        "operator_created_at",
        "operator_code",
        "operator_department",
        "operator_current_status",
        "operator_max_concurrent_chats",
        "conversation_id",
        "conversation_status",
        "conversation_priority",
        "conversation_started_at",
        "conversation_closed_at",
        "message_id",
        "message_content",
        "message_timestamp",
        "message_is_read",
        "attachment_id",
        "attachment_file_name",
        "attachment_file_size",
        "attachment_file_type",
    ]

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for idx in range(rows):
            conversation = random.choice(conversations)
            message_id = uuid4()
            message_timestamp = datetime.fromisoformat(conversation["conversation_started_at"]) + timedelta(
                minutes=random.randint(0, 1440)
            )

            has_attachment = random.random() < 0.3
            attachment_id = str(uuid4()) if has_attachment else ""

            row = {
                **conversation["client"],
                **conversation["operator"],
                "conversation_id": conversation["conversation_id"],
                "conversation_status": conversation["conversation_status"],
                "conversation_priority": conversation["conversation_priority"],
                "conversation_started_at": conversation["conversation_started_at"],
                "conversation_closed_at": conversation["conversation_closed_at"],
                "message_id": str(message_id),
                "message_content": _random_sentence(idx + 1),
                "message_timestamp": message_timestamp.isoformat(),
                "message_is_read": "true" if random.random() < 0.7 else "false",
                "attachment_id": attachment_id,
                "attachment_file_name": f"file_{idx + 1}.{random.choice(FILE_TYPES)}" if has_attachment else "",
                "attachment_file_size": str(random.randint(10_000, 5_000_000)) if has_attachment else "",
                "attachment_file_type": random.choice(FILE_TYPES) if has_attachment else "",
            }
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CSV data for the chat system.")
    parser.add_argument("--output", default="./chat_data.csv", help="Path to output CSV file")
    parser.add_argument("--rows", type=int, default=1000, help="Number of rows to generate")
    args = parser.parse_args()

    if args.rows < 1000:
        raise SystemExit("--rows must be at least 1000")

    generate_csv(args.output, args.rows)


if __name__ == "__main__":
    main()
