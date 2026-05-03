# bot.py
from aiogram import types
from sqlmodel import Session
from db import engine, Clients, create_all_table

from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

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


print("BOT MODULE LOADED")
create_all_table()  # Создаёт таблицы в БД при запуске бота, если их ещё нет

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

class AddClient(StatesGroup):
    contact_name = State()
    full_name = State()
    birthday = State()
    number = State()
    tg_link = State()
    fst_payment = State()
    client_goal = State()
    client_review = State()



router = Router()

@router.message(Command("add_client"))
async def start_add_client(message: types.Message, state: FSMContext):
    print("👉 /add_client TRIGGERED")  # 👈 СЮДА
    await message.answer("Введите контактное имя:")
    await state.set_state(AddClient.contact_name)

@router.message(AddClient.contact_name)
async def get_contact_name(message: types.Message, state: FSMContext):
    print("👉 contact_name STEP")  # 👈 СЮДА
    await state.update_data(contact_name=message.text)
    await message.answer("Введите полное имя:")
    await state.set_state(AddClient.full_name)

@router.message(AddClient.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    print("👉 full_name STEP")  # 👈 СЮДА
    await state.update_data(full_name=message.text)
    await message.answer("Введите дату рождения:")
    await state.set_state(AddClient.birthday)

@router.message(AddClient.birthday)
async def get_birthday(message: types.Message, state: FSMContext):
    print("👉 birthday STEP")  # 👈 СЮДА
    date_obj = parse_date(message.text)
    if not date_obj:
        await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    await state.update_data(birthday=date_obj)
    await message.answer("Введите номер телефона:")
    await state.set_state(AddClient.tg_link)

@router.message(AddClient.tg_link)
async def get_tg_link(message: types.Message, state: FSMContext):
    print("👉 tg_link STEP")  # 👈 СЮДА
    await state.update_data(tg_link=message.text)
    await message.answer("Введите ссылку на Telegram:")
    await state.set_state(AddClient.fst_payment)

@router.message(AddClient.fst_payment)
async def get_fst_payment(message: types.Message, state: FSMContext):
    print("👉 fst_payment STEP")  # 👈 СЮДА
    date_obj = parse_date(message.text)
    if not date_obj:
        await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    await state.update_data(birthday=date_obj)
    await message.answer("Дату первого платежа:")
    await state.set_state(AddClient.client_goal)

@router.message(AddClient.client_goal)
async def get_client_goal(message: types.Message, state: FSMContext):
    print("👉 client_goal STEP")  # 👈 СЮДА
    await state.update_data(client_goal=message.text)
    await message.answer("Цель клиента:")
    await state.set_state(AddClient.client_review)

@router.message(AddClient.client_review)
async def get_client_review(message: types.Message, state: FSMContext):
    print("👉 client_review STEP")  # 👈 СЮДА
    await state.update_data(client_review=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(AddClient.number)

@router.message(AddClient.number)
async def get_number(message: types.Message, state: FSMContext):
    data = await state.update_data(number=message.text)

    with Session(engine) as ses:
        client = Clients(
            contact_name=data["contact_name"],
            full_name=data["full_name"],
            birthday=data["birthday"],
            tg_link=data["tg_link"],
            number=data["number"], 
            fst_payment=data["fst_payment"],
            client_goal=data["client_goal"],
            client_review=data["client_review"]
        )
        ses.add(client)
        ses.commit()

    await message.answer("✅ Клиент успешно добавлен!")
    await state.clear()

# ---------- NEXT- ---------

# async def cmd_add_client(message: types.Message):
#     parts = message.text.split(maxsplit=2)
#     if len(parts) < 2:
#         await message.answer("Использование: /add_client Имя [Телефон]")
#         return

#     name = parts[1]
#     phone = parts[2] if len(parts) > 2 else None

#     with Session() as ses:
#         client = Client(name=name, phone=phone)
#         ses.add(client)
#         ses.commit()
#         await message.answer(f"Клиент добавлен: {client.name}, ID={client.id}")


###### /add_visit ######

# async def cmd_add_visit(message: types.Message):
#     parts = message.text.split(maxsplit=3)
#     if len(parts) < 3:
#         await message.answer("Использование: /add_visit ID_клиента ДД-ММ-ГГГГ [Примечание]")
#         return

#     try:
#         client_id = int(parts[1])
#     except ValueError:
#         await message.answer("ID клиента должен быть числом.")
#         return

#     date_str = parts[2]
#     date_obj = parse_date(date_str)
#     if not date_obj:
#         await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
#         return

#     note = parts[3] if len(parts) > 3 else None

#     with Session() as ses:
#         client = ses.get(Clients, client_id)
#         if not client:
#             await message.answer("Клиент не найден.")
#             return

#         visit = Visits(client_id=client_id, visit_date=date_obj, note=note)
#         ses.add(visit)
#         ses.commit()
#         await message.answer(f"Визит добавлен: {client.name} ({date_obj})")


###### /add_schedule ######

# async def cmd_add_schedule(message: types.Message):
#     parts = message.text.split(maxsplit=4)
#     if len(parts) < 4:
#         await message.answer("Использование: /add_schedule ДД-ММ-ГГГГ НАЧАЛО КОНЕЦ [Примечание]")
#         return

#     date_str = parts[1]
#     start_time = parts[2]
#     end_time = parts[3]
#     note = parts[4] if len(parts) > 4 else None

#     date_obj = parse_date(date_str)
#     if not date_obj:
#         await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
#         return

#     with Session() as ses:
#         sched = Schedule(
#             date=date_obj,
#             start_time=start_time,
#             end_time=end_time,
#             note=note
#         )
#         ses.add(sched)
#         ses.commit()
#         await message.answer(f"Расписание добавлено: {date_obj} {start_time}–{end_time}")


# ###### /change_product ######

# async def cmd_change_product(message: types.Message):
#     parts = message.text.split(maxsplit=3)
#     if len(parts) < 3:
#         await message.answer("Использование: /change_product ID_продукта НОВОЕ_ИМЯ НОВАЯ_ЦЕНА")
#         return

#     try:
#         prod_id = int(parts[1])
#     except ValueError:
#         await message.answer("ID продукта должен быть числом.")
#         return

#     name = parts[2]
#     try:
#         price = int(parts[3])
#     except ValueError:
#         await message.answer("Цена должна быть числом.")
#         return

#     with Session() as ses:
#         prod = ses.get(Products, prod_id)
#         if not prod:
#             await message.answer("Продукт не найден.")
#             return

#         prod.name = name
#         prod.price = price
#         ses.commit()
#         await message.answer(f"Продукт изменён: {name} = {price} ₽")


###### /active_clients /inactive_clients ######

# async def cmd_active_clients(message: types.Message):
#     with Session() as ses:
#         stmt = select(Clients).where(Clients.is_active.is_(True))
#         rows = ses.execute(stmt).scalars().all()
#         if rows:
#             text = "Активные клиенты:\n" + "\n".join(
#                 f"{c.id} {c.name} ({c.phone or 'нет телефона'})"
#                 for c in rows
#             )
#         else:
#             text = "Нет активных клиентов."
#         await message.answer(text)


# async def cmd_inactive_clients(message: types.Message):
#     with Session() as ses:
#         stmt = select(Clients).where(Clients.is_active.is_(False))
#         rows = ses.execute(stmt).scalars().all()
#         if rows:
#             text = "Неактивные клиенты:\n" + "\n".join(
#                 f"{c.id} {c.name} ({c.phone or 'нет телефона'})"
#                 for c in rows
#             )
#         else:
#             text = "Нет неактивных клиентов."
#         await message.answer(text)


###### /schedule ######

# async def cmd_schedule(message: types.Message):
#     with Session() as ses:
#         stmt = select(Schedule).order_by(Schedule.date)
#         rows = ses.execute(stmt).scalars().all()
#         if rows:
#             text = "Расписание:\n" + "\n".join(
#                 f"{s.date} {s.start_time}–{s.end_time} {s.note or ''}"
#                 for s in rows
#             )
#         else:
#             text = "Расписание пусто."
#         await message.answer(text)


###### /products ######

# async def cmd_products(message: types.Message):
#     with Session() as ses:
#         stmt = select(Products).where(Products.is_active.is_(True))
#         rows = ses.execute(stmt).scalars().all()
#         if rows:
#             text = "Товары:\n" + "\n".join(
#                 f"{p.id} {p.name} = {p.price} ₽"
#                 for p in rows
#             )
#         else:
#             text = "Нет товаров."
#         await message.answer(text)


###### Регистрация хендлеров ######

# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(cmd_start, commands=["start"])
#     dp.register_message_handler(cmd_help, commands=["help"])
#     # dp.register_message_handler(cmd_add_client, lambda m: m.text.startswith("/add_client"))
#     dp.register_message_handler(cmd_add_visit, lambda m: m.text.startswith("/add_visit"))
#     dp.register_message_handler(cmd_add_schedule, lambda m: m.text.startswith("/add_schedule"))
#     dp.register_message_handler(cmd_change_product, lambda m: m.text.startswith("/change_product"))
#     dp.register_message_handler(cmd_active_clients, commands=["active_clients"])
#     dp.register_message_handler(cmd_inactive_clients, commands=["inactive_clients"])
#     dp.register_message_handler(cmd_schedule, commands=["schedule"])
#     dp.register_message_handler(cmd_products, commands=["products"])
