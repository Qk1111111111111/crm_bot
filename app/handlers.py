from aiogram import Router, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F

from repo.db import create_client
import app.keyboards as kb

from utils import parse_date, normalize_ru_phone
from keys import HELP_TEXT    

import logging


logger = logging.getLogger(__name__)
router = Router()


logger.info("Bot module loaded")


# -------- START / HELP / CANCEL -------
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("CRM-бот запущен.\n\n" + HELP_TEXT, reply_markup=kb.main)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)

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
        await message.answer("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
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
    contact_name = State()
    full_name = State()
    birthday = State()
    number = State()
    tg_link = State()
    fst_payment = State()

@router.message(Command("add_vpt"))
async def start_add_vpt(message: types.Message, state: FSMContext):
    logger.info("👉 /add_vpt TRIGGERED")
    await message.answer("Введите контактное имя:")
    await state.set_state(AddVPT.contact_name)