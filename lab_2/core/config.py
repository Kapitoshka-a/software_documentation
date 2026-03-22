from pydantic_settings import BaseSettings
from sqlalchemy import Engine
from sqlmodel import create_engine, Session, SQLModel
from typing import Iterator


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./support_chat.db"
    CSV_PATH: str = "./chat_data.csv"

    def get_engine(self) -> Engine:
        return create_engine(self.DATABASE_URL)

    def get_sqlite_session(self) -> Iterator[Session]:
        with Session(self.get_engine()) as session:
            yield session

    def create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self.get_engine())

    class Config:
        env_file = ".env"


settings = Settings()
