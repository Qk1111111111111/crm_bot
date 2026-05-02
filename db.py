import asyncio
import os
import psycopg
import sqlalchemy

from datetime import datetime, time
from typing import Type
from sqlalchemy import Table, Column, Integer, String
from sqlmodel import create_engine, SQLModel, Field, MetaData, select, Session
from sqlalchemy.ext.asyncio import create_async_engine



import keys as const


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def is_alive(conn):
    if conn is None or conn.closed:
        return False
    try:
        await conn.set_autocommit(False)
        cur = conn.cursor()
        await cur.execute("CREATE TEMP TABLE tmp_write_test(id INT);")
        await cur.execute("INSERT INTO tmp_write_test VALUES (1);")
        await conn.rollback()
        await cur.close()
        return True
    except (psycopg.OperationalError, psycopg.ProgrammingError, psycopg.errors.ReadOnlySqlTransaction) as e:
        return False


def keys(db_user=None, db_pass=None, db_host=None):
    if db_host is None:
        db_host = const.DB_HOST
        # db_host = os.getenv("DB_HOST")
    if db_user is None:
        db_user = const.LOG
        # db_user = os.getenv("DB_USER")
    if db_pass is None:
        db_pass = const.PASS
        # db_pass = os.getenv("DB_PASS")
    return db_host, db_user, db_pass


def create_temp_table(engine):
    """Создает временную таблицу."""
    metadata = MetaData()
    temp_table = Table(
        "temp_table",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("value", String),
    )

    try:
        with engine.connect() as connection:
            temp_table.create(bind=engine)
            return temp_table
    except (psycopg.OperationalError, psycopg.ProgrammingError, psycopg.errors.ReadOnlySqlTransaction,
            sqlalchemy.exc.InternalError) as e:
        return None


def is_read_only(engine):
    temp_table = create_temp_table(engine)  # Создаем таблицу здесь
    if temp_table is None:
        return True  # Если не удалось создать таблицу, считаем хост только для чтения

    try:
        with engine.connect() as connection:
            connection.execute(temp_table.insert().values(value="test data"))
            return False  # Запись прошла успешно - хост для записи
    except Exception as e:
        return True  # Ошибка записи - хост только для чтения
    finally:
        # Убеждаемся, что таблица удалена
        try:
            with engine.connect() as connection:
                temp_table.drop(bind=engine)
        except Exception as e:
            print(f"Ошибка при удалении временной таблицы: {e}")


def get_engine(*args, **kwargs, ):
    db_host, db_user, db_pass = keys(*args, **kwargs)
    db_port = const.DB_PORT
    db_database = const.DB_DATABASE
    hosts = db_host.split(',')
    for host in hosts:
        url = f'postgresql+psycopg://{db_user}:{db_pass}@{host}:{db_port}/{db_database}'
        if is_read_only(create_engine(url)):
            continue
        url = f'postgresql+asyncpg://{db_user}:{db_pass}@{host}:{db_port}/{db_database}'
        break
    else:
        raise Exception("Не удалось подключиться ни к одному из хостов")

    return create_async_engine(url,
                               pool_pre_ping=True,
                               pool_size=10,
                               max_overflow=20,
                               pool_recycle=1800, )


def get_sync_engine(*args, **kwargs, ):
    db_host, db_user, db_pass = keys(*args, **kwargs)
    db_port = const.DB_PORT
    db_database = const.DB_DATABASE
    db_host, *_ = db_host.split(',')
    url = f'postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_database}'

    return create_engine(url), url

engine, DB_URL = get_sync_engine()

# class Base(SQLModel):
#     metadata = MetaData(schema=const.DB_SCHEMA)


class Products(SQLModel, table=True):
    __tablename__ = 'products'
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    product_id: str = Field(default=None)
    name: str = Field(default=None)
    description: str = Field(default=None)
    price: int = Field(default=None)
    number: str = Field(default=None)
    time_frame: datetime = Field(default=None)
    status: str = Field(default=None)


class Clients(SQLModel, table=True):
    __tablename__ = "clients"
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    telegram_id: int = Field(default=None, unique=True)  # можно использоваться позже для связи с Telegram
    contact_name: str = Field(default=None)
    full_name: str = Field(default=None)
    birthday: datetime = Field(default=None)
    number: str = Field(default=None)
    fst_payment: datetime = Field(default=None)
    last_contact: datetime = Field(default=None)
    status: str = Field(default=None)   
    created_at: datetime = Field(default=datetime.now())


# class Payments(Base):
#     __tablename__ = "payments"
#     id: int = Field(default=None, primary_key=True)
#     client_id: str = Field(default=None)  # можно использоваться позже для связи с Telegram
#     product_id: str = Field(default=None)
#     amount: int = Field(default=None)
#     created_at: datetime = Field(default=datetime.now())
#     payment_method: str = Field(default=None)
#     comment: str = Field(default=None)


# class Visits(Base):
#     __tablename__ = "visits"
#     id: int = Field(default=None, primary_key=True)
#     client_id: str = Field(default=None)
#     scheduled_date: datetime = Field(default=None)
#     attended: bool = Field(default=False)
#     comments: int = Field(default=None)
#     created_at: datetime = Field(default=datetime.now())


# class Schedule(Base):
#     __tablename__ = "schedule"
#     id: int = Field(default=None, primary_key=True)
#     shedule_date: datetime = Field(default=None)
#     dw: bool = Field(default=False)
#     work_start: time = Field(default=None)
#     break_start: time = Field(default=None)
#     break_end: time = Field(default=None)
#     work_end: time = Field(default=None)
#     break_duration: int = Field(default=None)
#     working_hours: int = Field(default=None)



def all_item(table: type[SQLModel], lim: int | None = None):
    with Session(engine) as session:
        statement = select(table)

        if lim:
            statement = statement.limit(lim)

        return session.exec(statement).all()
    

def create_all_table():
    sync_engine, *_ = get_sync_engine()
    SQLModel.metadata.create_all(sync_engine)
    print("done")



if __name__ == '__main__':
    create_all_table()