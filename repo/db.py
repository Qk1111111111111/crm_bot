from datetime import datetime, time
from sqlmodel import create_engine, SQLModel, Field, select, Session

import keys as const

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
    tg_link: str | None = Field(default=None)
    contact_name: str | None = Field(default=None)
    full_name: str | None = Field(default=None)
    birthday: datetime | None = Field(default=None)
    number: str | None = Field(default=None)
    fst_payment: datetime | None = Field(default=None)
    last_contact: datetime | None = Field(default=None)
    status: str | None = Field(default='new')
    created_at: datetime = Field(default_factory=datetime.now)


class ClientVpt(SQLModel, table=True):
    __tablename__ = "client_vpt"
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    client_id: int | None = Field(default=None)
    mood_txt: str | None = Field(default=None)
    training_history: str | None = Field(default=None)
    health_complaints: str | None = Field(default=None)
    fitness_goals: str | None = Field(default=None)
    expected_life_changes: str | None = Field(default=None)
    goal_details: str | None = Field(default=None)
    training_frequency: str | None = Field(default=None)
    product_id: int | None = Field(default=None)
    next_session_date: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)


class Payments(SQLModel, table=True):
    __tablename__ = "payments"
    __table_args__ = {"schema": const.DB_SCHEMA}
    id: int = Field(default=None, primary_key=True)
    client_id: int | None = Field(default=None)
    product_id: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    payment_method: str | None = Field(default=None)
    comment: str | None = Field(default=None)
    payment_date: datetime | None = Field(default=None)


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

def create_client(client_data: dict) -> Clients:
    with Session(engine) as ses:
        client = Clients(
            contact_name=client_data["contact_name"],
            full_name=client_data["full_name"],
            birthday=client_data["birthday"],
            number=client_data["number"],
            tg_link=client_data["tg_link"],
            fst_payment=client_data["fst_payment"]
        )
        ses.add(client)
        ses.commit()
        ses.refresh(client)
        return client
    
def create_vpt(vpt_data: dict) -> ClientVpt:
    with Session(engine) as ses:
        vpt = ClientVpt(
            client_id = vpt_data["client_id"],
            mood_txt=vpt_data["mood_txt"],
            training_history=vpt_data["training_history"],
            health_complaints=vpt_data["health_complaints"],
            fitness_goals=vpt_data["fitness_goals"],
            expected_life_changes=vpt_data["expected_life_changes"],
            goal_details=vpt_data["goal_details"],
            training_frequency=vpt_data["training_frequency"],
            product_id=vpt_data["product_id"],
            next_session_date=vpt_data["next_session_date"]
        )
        ses.add(vpt)
        ses.commit()
        ses.refresh(vpt)
        return vpt
    
def create_payment(payment_data: dict) -> Payments:
    with Session(engine) as ses:
        payment = Payments(
            client_id=payment_data["client_id"],
            product_id=payment_data["product_id"],
            payment_method=payment_data["payment_method"],
            payment_date=payment_data["payment_date"],
            comment=payment_data["comment"]
        )
        ses.add(payment)
        ses.commit()
        ses.refresh(payment)
        return payment  
    
def create_visit(visit_data: dict) -> Visits:
    with Session(engine) as ses:
        visit = Visits(
            client_id=visit_data["client_id"],
            scheduled_date=visit_data["scheduled_date"],
            attended=visit_data["attended"],
            comment=visit_data["comment"]
        )
        ses.add(visit)
        ses.commit()
        ses.refresh(visit)
        return visit
 

if __name__ == '__main__':
    create_all_table()