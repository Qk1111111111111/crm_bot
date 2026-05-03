import asyncio
import os

from datetime import datetime, time
from sqlmodel import create_engine, SQLModel, Field, select, Session
from sqlalchemy import Column, String

import keys as const


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


DB_URL = f"postgresql+psycopg://{const.LOG}:{const.PASS}@{const.DB_HOST}:{const.DB_PORT}/{const.DB_DATABASE}"
engine = create_engine(DB_URL)


class Products(SQLModel, table=True):
    __tablename__ = 'products'
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    product_id: str | None = Field(default=None)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    number: str | None = Field(default=None)
    time_frame: datetime | None = Field(default=None)
    status: str | None = Field(default=None)


class Clients(SQLModel, table=True):
    __tablename__ = "clients"
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    telegram_id: int | None = Field(default=None, sa_column=Column(String, unique=True))
    contact_name: str | None = Field(default=None)
    full_name: str | None = Field(default=None)
    birthday: datetime | None = Field(default=None)
    number: str | None = Field(default=None)
    fst_payment: datetime | None = Field(default=None)
    last_contact: datetime | None = Field(default=None)
    status: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)


class Payments(SQLModel, table=True):
    __tablename__ = "payments"
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    client_id: str | None = Field(default=None)
    product_id: str | None = Field(default=None)
    amount: int | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    payment_method: str | None = Field(default=None)
    comment: str | None = Field(default=None)


class Visits(SQLModel, table=True):
    __tablename__ = "visits"
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    client_id: str | None = Field(default=None)
    scheduled_date: datetime | None = Field(default=None)
    attended: bool = Field(default=False)
    comment: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)


class Schedule(SQLModel, table=True):
    __tablename__ = "schedule"
    __table_args__ = {"schema": const.DB_SCHEMA}
    date: datetime = Field(default=None, primary_key=True)
    dw: bool = Field(default=False)
    work_start: time | None = Field(default=None)
    break_start: time | None = Field(default=None)
    break_end: time | None = Field(default=None)
    work_end: time | None = Field(default=None)
    break_duration: int | None = Field(default=None)
    working_hours: int | None = Field(default=None)


def all_item(table: type[SQLModel], lim: int | None = None):
    with Session(engine) as session:
        statement = select(table)
        if lim is not None:
            statement = statement.limit(lim)
        return session.exec(statement).all()
    

def create_all_table():
    SQLModel.metadata.create_all(engine)
    print("Модели БД загружены эхей баля -- done")


if __name__ == '__main__':
    create_all_table()