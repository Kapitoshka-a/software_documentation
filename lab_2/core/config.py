from pydantic_settings import BaseSettings
from sqlalchemy import Engine
from sqlmodel import create_engine, Session, SQLModel
from typing import Iterator


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./support_chat.db"
    CSV_PATH: str = "./chat_data.csv"

    EXPORTER_STRATEGY: str = "redis"
    EXPORTER_DATA_FILE: str = "data.json"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_NAMESPACE: str = "support_chat"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "support_chat"

    def get_engine(self) -> Engine:
        return create_engine(self.DATABASE_URL)

    def get_sqlite_session(self) -> Iterator[Session]:
        with Session(self.get_engine()) as session:
            yield session

    def create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self.get_engine())

    class ConfigDict:
        env_file = ".env"


settings = Settings()
