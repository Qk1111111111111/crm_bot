# bot.py
from aiogram import types
from aiogram.dispatcher import Dispatcher
from sqlalchemy import select
from db import Session, Client, Visit, Schedule, Product


HELP_TEXT = """
/delpay - добавить оплату
/add_client Имя Телефон
/add_visit ID_клиента ДД-ММ-ГГГГ Примечание
/add_schedule ДД-ММ-ГГГГ НАЧАЛО КОНЕЦ Примечание
/change_product ID_продукта НОВОЕ_ИМЯ НОВАЯ_ЦЕНА
/active_clients
/inactive_clients
/schedule
/products
"""


async def cmd_start(message: types.Message):
    await message.answer("CRM‑бот запущен.\n\n" + HELP_TEXT)


async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)


def parse_date(s):
    from datetime import datetime
    try:
        return datetime.strptime(s, "%d-%m-%Y").date()
    except (ValueError, TypeError):
        return None


###### /add_client ######

async def cmd_add_client(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        await message.answer("Использование: /add_client Имя [Телефон]")
        return

    name = parts[1]
    phone = parts[2] if len(parts) > 2 else None

    with Session() as ses:
        client = Client(name=name, phone=phone)
        ses.add(client)
        ses.commit()
        await message.answer(f"Клиент добавлен: {client.name}, ID={client.id}")


###### /add_visit ######

async def cmd_add_visit(message: types.Message):
    parts = message.text.split(maxsplit=3)
    if len(parts) < 3:
        await message.answer("Использование: /add_visit ID_клиента ДД-ММ-ГГГГ [Примечание]")
        return

    try:
        client_id = int(parts[1])
    except ValueError:
        await message.answer("ID клиента должен быть числом.")
        return

    date_str = parts[2]
    date_obj = parse_date(date_str)
    if not date_obj:
        await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
        return

    note = parts[3] if len(parts) > 3 else None

    with Session() as ses:
        client = ses.get(Client, client_id)
        if not client:
            await message.answer("Клиент не найден.")
            return

        visit = Visit(client_id=client_id, visit_date=date_obj, note=note)
        ses.add(visit)
        ses.commit()
        await message.answer(f"Визит добавлен: {client.name} ({date_obj})")


###### /add_schedule ######

async def cmd_add_schedule(message: types.Message):
    parts = message.text.split(maxsplit=4)
    if len(parts) < 4:
        await message.answer("Использование: /add_schedule ДД-ММ-ГГГГ НАЧАЛО КОНЕЦ [Примечание]")
        return

    date_str = parts[1]
    start_time = parts[2]
    end_time = parts[3]
    note = parts[4] if len(parts) > 4 else None

    date_obj = parse_date(date_str)
    if not date_obj:
        await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
        return

    with Session() as ses:
        sched = Schedule(
            date=date_obj,
            start_time=start_time,
            end_time=end_time,
            note=note
        )
        ses.add(sched)
        ses.commit()
        await message.answer(f"Расписание добавлено: {date_obj} {start_time}–{end_time}")


###### /change_product ######

async def cmd_change_product(message: types.Message):
    parts = message.text.split(maxsplit=3)
    if len(parts) < 3:
        await message.answer("Использование: /change_product ID_продукта НОВОЕ_ИМЯ НОВАЯ_ЦЕНА")
        return

    try:
        prod_id = int(parts[1])
    except ValueError:
        await message.answer("ID продукта должен быть числом.")
        return

    name = parts[2]
    try:
        price = int(parts[3])
    except ValueError:
        await message.answer("Цена должна быть числом.")
        return

    with Session() as ses:
        prod = ses.get(Product, prod_id)
        if not prod:
            await message.answer("Продукт не найден.")
            return

        prod.name = name
        prod.price = price
        ses.commit()
        await message.answer(f"Продукт изменён: {name} = {price} ₽")


###### /active_clients /inactive_clients ######

async def cmd_active_clients(message: types.Message):
    with Session() as ses:
        stmt = select(Client).where(Client.is_active.is_(True))
        rows = ses.execute(stmt).scalars().all()
        if rows:
            text = "Активные клиенты:\n" + "\n".join(
                f"{c.id} {c.name} ({c.phone or 'нет телефона'})"
                for c in rows
            )
        else:
            text = "Нет активных клиентов."
        await message.answer(text)


async def cmd_inactive_clients(message: types.Message):
    with Session() as ses:
        stmt = select(Client).where(Client.is_active.is_(False))
        rows = ses.execute(stmt).scalars().all()
        if rows:
            text = "Неактивные клиенты:\n" + "\n".join(
                f"{c.id} {c.name} ({c.phone or 'нет телефона'})"
                for c in rows
            )
        else:
            text = "Нет неактивных клиентов."
        await message.answer(text)


###### /schedule ######

async def cmd_schedule(message: types.Message):
    with Session() as ses:
        stmt = select(Schedule).order_by(Schedule.date)
        rows = ses.execute(stmt).scalars().all()
        if rows:
            text = "Расписание:\n" + "\n".join(
                f"{s.date} {s.start_time}–{s.end_time} {s.note or ''}"
                for s in rows
            )
        else:
            text = "Расписание пусто."
        await message.answer(text)


###### /products ######

async def cmd_products(message: types.Message):
    with Session() as ses:
        stmt = select(Product).where(Product.is_active.is_(True))
        rows = ses.execute(stmt).scalars().all()
        if rows:
            text = "Товары:\n" + "\n".join(
                f"{p.id} {p.name} = {p.price} ₽"
                for p in rows
            )
        else:
            text = "Нет товаров."
        await message.answer(text)


###### Регистрация хендлеров ######

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_help, commands=["help"])
    dp.register_message_handler(cmd_add_client, lambda m: m.text.startswith("/add_client"))
    dp.register_message_handler(cmd_add_visit, lambda m: m.text.startswith("/add_visit"))
    dp.register_message_handler(cmd_add_schedule, lambda m: m.text.startswith("/add_schedule"))
    dp.register_message_handler(cmd_change_product, lambda m: m.text.startswith("/change_product"))
    dp.register_message_handler(cmd_active_clients, commands=["active_clients"])
    dp.register_message_handler(cmd_inactive_clients, commands=["inactive_clients"])
    dp.register_message_handler(cmd_schedule, commands=["schedule"])
    dp.register_message_handler(cmd_products, commands=["products"])
