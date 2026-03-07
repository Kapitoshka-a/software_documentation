from sqlmodel import Session

from serializers.import_bundle import ImportBundle
from core.interfaces import RepositoryInterface


class ImportRepository(RepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save_bundle(self, bundle: ImportBundle) -> None:
        for user in bundle.users:
            self._session.merge(user)
        for client in bundle.clients:
            self._session.merge(client)
        for operator in bundle.operators:
            self._session.merge(operator)
        for conversation in bundle.conversations:
            self._session.merge(conversation)
        for message in bundle.messages:
            self._session.merge(message)
        for attachment in bundle.attachments:
            self._session.merge(attachment)
        self._session.commit()
