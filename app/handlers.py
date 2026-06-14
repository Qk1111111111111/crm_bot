from aiogram import Router, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F

from repo.db import create_client, create_vpt, create_payment
import app.keyboards as kb

from utils import parse_date, normalize_ru_phone
import keys as const 

import logging


logger = logging.getLogger(__name__)
router = Router()


logger.info("Bot module loaded")


# -------- START / HELP / CANCEL -------
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("CRM-бот запущен.\n\n" + const.HELP_TEXT, reply_markup=kb.main)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(const.HELP_TEXT)

@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Текущее действие отменено.", reply_markup=kb.main)


# -------- /add_client -------
class AddClient(StatesGroup):
    contact_name = State()
    full_name = State()
    birthday = State()
    number = State()
    tg_link = State()
    fst_payment = State()

async def start_add_client_flow(message: types.Message, state: FSMContext):
    logger.info("👉 /add_client TRIGGERED")
    await message.answer("Введите контактное имя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddClient.contact_name)

@router.message(Command("add_client"))
async def start_add_client(message: types.Message, state: FSMContext):
    await start_add_client_flow(message, state)


@router.message(F.text == "Добавить клиента")
async def add_client_from_button(message: types.Message, state: FSMContext):
    await start_add_client_flow(message, state)


@router.message(AddClient.contact_name)
async def get_contact_name(message: types.Message, state: FSMContext):
    logger.info("👉 contact_name STEP")
    await state.update_data(contact_name=message.text)
    await message.answer("Введите полное имя:")
    await state.set_state(AddClient.full_name)

@router.message(AddClient.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    logger.info("👉 full_name STEP")
    await state.update_data(full_name=message.text)
    await message.answer("Введите дату рождения:")
    await state.set_state(AddClient.birthday)

@router.message(AddClient.birthday)
async def get_birthday(message: types.Message, state: FSMContext):
    logger.info("👉 birthday STEP")  # 👈 СЮДА
    date_obj = parse_date(message.text)
    if not date_obj:
        await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    await state.update_data(birthday=date_obj)
    await message.answer("Введите номер телефона:")
    await state.set_state(AddClient.number)

@router.message(AddClient.number)
async def get_number(message: types.Message, state: FSMContext):
    logger.info("👉 number STEP")  # 👈 СЮДА
    normalized = normalize_ru_phone(message.text)
    if not normalized:  
        await message.answer("Неверный формат номера. Введите российский номер телефона.")
        return
    await state.update_data(number=normalized)
    await message.answer("Введите ссылку на Telegram:")
    await state.set_state(AddClient.tg_link)

@router.message(AddClient.tg_link)
async def get_tg_link(message: types.Message, state: FSMContext):
    logger.info("👉 tg_link STEP")  # 👈 СЮДА
    await state.update_data(tg_link=message.text)
    await message.answer("Введите дату первого платежа:")
    await state.set_state(AddClient.fst_payment)

@router.message(AddClient.fst_payment)
async def get_fst_payment(message: types.Message, state: FSMContext):
    logger.info("👉 fst_payment STEP")  # 👈 СЮДА
    date_obj = parse_date(message.text)
    if not date_obj:
        date_obj = parse_date('2999-12-31')
    data = await state.update_data(fst_payment=date_obj)
    try:
        create_client(data)
        await message.answer("✅ Клиент успешно добавлен!", reply_markup=kb.main)
        await state.clear()
    except Exception:
        logger.exception("Error while creating client")
        await message.answer("❌ Не удалось сохранить клиента. Попробуйте ещё раз.")

# -------- /add_vpt -------
class AddVPT(StatesGroup):
    client_id=State()
    mood_txt = State()
    training_history = State()
    health_complaints = State()
    fitness_goals = State()
    expected_life_changes = State()
    goal_details = State()
    training_frequency = State()
    product_id = State()
    next_session_date = State()
    payment_date = State()

async def add_vpt_flow(message: types.Message, state: FSMContext):
    logger.info("👉 /add_vpt TRIGGERED")
    await message.answer(const.CLIENT_ID, reply_markup=await kb.clients_kb())
    await state.set_state(AddVPT.client_id)

@router.message(Command("add_vpt"))
async def start_add_vpt(message: types.Message, state: FSMContext):
    await add_vpt_flow(message, state)

@router.message(F.text == "Анкета ВПТ")
async def add_vpt_from_button(message: types.Message, state: FSMContext):
    await add_vpt_flow(message, state)

@router.callback_query(AddVPT.client_id, F.data.startswith("client:"))
async def client_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    client_id = int(callback.data.split(":")[1])
    logger.info(f"КЛИЕНТ №{client_id}")
    await state.update_data(client_id=client_id)
    await callback.message.answer(const.MOOD_TXT)
    await state.set_state(AddVPT.mood_txt)

@router.message(AddVPT.mood_txt)
async def get_mood_txt(message: types.Message, state: FSMContext):
    logger.info("👉 mood_txt STEP")
    await state.update_data(mood_txt=message.text)
    await message.answer(const.TRAINING_HISTORY)
    await state.set_state(AddVPT.training_history)

@router.message(AddVPT.training_history)
async def get_training_history(message: types.Message, state: FSMContext):
    logger.info("👉 training_history STEP")
    await state.update_data(training_history=message.text)
    await message.answer(const.HEALTH_COMPLAINTS)
    await state.set_state(AddVPT.health_complaints)

@router.message(AddVPT.health_complaints)
async def get_health_complaints(message: types.Message, state: FSMContext):
    logger.info("👉 health_complaints STEP")
    await state.update_data(health_complaints=message.text)
    await message.answer(const.FITNESS_GOALS)
    await state.set_state(AddVPT.fitness_goals)

@router.message(AddVPT.fitness_goals)
async def get_fitness_goals(message: types.Message, state: FSMContext):
    logger.info("👉 fitness_goals STEP")
    await state.update_data(fitness_goals=message.text)
    await message.answer(const.EXPECTED_LIFE_CHANGES)
    await state.set_state(AddVPT.expected_life_changes) 

@router.message(AddVPT.expected_life_changes)
async def get_expected_life_changes(message: types.Message, state: FSMContext):
    logger.info("👉 expected_life_changes STEP")
    await state.update_data(expected_life_changes=message.text)
    await message.answer(const.GOAL_DETAILS)
    await state.set_state(AddVPT.goal_details)

@router.message(AddVPT.goal_details)
async def get_goal_details(message: types.Message, state: FSMContext):
    logger.info("👉 goal_details STEP")
    await state.update_data(goal_details=message.text)
    await message.answer(const.TRAINING_FREQUENCY)
    await state.set_state(AddVPT.training_frequency)

@router.message(AddVPT.training_frequency)
async def get_training_frequency(message: types.Message, state: FSMContext):
    logger.info("👉 training_frequency STEP")
    await state.update_data(training_frequency=message.text)
    await message.answer(const.PRODUCT_ID, reply_markup=await kb.products_kb())
    await state.set_state(AddVPT.product_id)

@router.callback_query(AddVPT.product_id, F.data.startswith("product:"))
async def client_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    product_id = int(callback.data.split(":")[1])
    await state.update_data(product_id=product_id)
    await callback.message.answer(const.NEXT_SESSION_DATE)
    await state.set_state(AddVPT.next_session_date)

@router.message(AddVPT.next_session_date)
async def get_next_session_date(message: types.Message, state: FSMContext):
    logger.info("👉 next_session_date STEP")
    date_obj = parse_date(message.text)
    if not date_obj:
        await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    await state.update_data(next_session_date=date_obj)
    await message.answer(const.PAYMENT_DATE)
    await state.set_state(AddVPT.payment_date)  

@router.message(AddVPT.payment_date)
async def get_payment_date(message: types.Message, state: FSMContext):
    logger.info("👉 payment_date STEP")
    date_obj = parse_date(message.text)
    if not date_obj:
        await message.answer("2999-12-31")
        return
    data = await state.update_data(payment_date=date_obj)
    try:
        create_vpt(data)
        await message.answer("✅ ВПТ клиента успешно добавлено!", reply_markup=kb.main)
        await state.clear()
    except Exception:
        logger.exception("Error while creating client")
        await message.answer("❌ Не удалось сохранить ВПТ клиента. Попробуйте ещё раз.")


# -------- /add_payment -------
class AddPayment(StatesGroup):
    client_id = State()
    product_id = State()
    comment = State()


async def add_payment_flow(message: types.Message, state: FSMContext):
    logger.info("👉 /add_payment TRIGGERED")
    await message.answer(const.CLIENT_ID, reply_markup=await kb.clients_payment())
    await state.set_state(AddPayment.client_id)

@router.message(Command("add_payment"))
async def start_add_payment(message: types.Message, state: FSMContext):
    await add_payment_flow(message, state)

@router.message(F.text == "Записать оплату")
async def add_payment_from_button(message: types.Message, state: FSMContext):
    await add_payment_flow(message, state)

@router.callback_query(AddPayment.client_id, F.data.startswith("client:"))
async def client_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    client_id = int(callback.data.split(":")[1])
    logger.info(f"КЛИЕНТ №{client_id}")
    await state.update_data(client_id=client_id)
    await callback.message.answer(const.PRODUCT_ID, reply_markup=await kb.products_kb())
    await state.set_state(AddPayment.product_id)

@router.callback_query(AddPayment.product_id, F.data.startswith("product:"))
async def product_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    product_id = int(callback.data.split(":")[1])
    await state.update_data(product_id=product_id)
    await callback.message.answer(const.COMMENT)
    await state.set_state(AddPayment.comment)

@router.message(AddPayment.comment)
async def payment_comment(message: types.Message, state: FSMContext):
    logger.info("👉 comment STEP")
    comment =await state.update_data(comment=message.text)
    data = await state.update_data(payment_date=comment)
    try:
        create_payment(data)
        await message.answer("✅ Оплата успешно добавлена!", reply_markup=kb.main)
        await state.clear()
    except Exception:
        logger.exception("Error while creating client")
        await message.answer("❌ Не удалось сохранить оплату. Попробуйте ещё раз.")