import uuid
from typing import Dict

from pydantic import BaseModel
from sqlalchemy import Engine, JSON, Column
from sqlmodel import Session, SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_external: uuid.UUID = Field(default_factory=uuid.uuid4)
    wallet_address: str


class Response(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: Dict = Field(default_factory=dict, sa_column=Column(JSON))


class Repository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def create_user(self, *, wallet_address: str) -> User:
        user = User(wallet_address=wallet_address)

        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)

        return user

    def create_response(self, *, data: dict) -> Response:
        response = Response(data=data)

        with Session(self.engine) as session:
            session.add(response)
            session.commit()
            session.refresh(response)

        return response
