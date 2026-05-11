from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder 
from repo.db import all_item, Clints

main = ReplyKeyboardMarkup([
    [KeyboardButton(text='Поставить тренировку в расписание')],
    [KeyboardButton(text='Новый клиент'), KeyboardButton(text='Анкета ВПТ')],
    [KeyboardButton(text='Записать оплату')]
],
        resize_keyboard=True, 
        input_field_placeholder='Выбери пункт меню'
)

async def clients_kb():
    clients = all_item(Clints)
    builder = ReplyKeyboardBuilder()
    for client in clients:
        builder.add(KeyboardButton(text=client.full_name))
    builder.add(KeyboardButton(text='Назад'))
    return builder.adjust(1).as_markup(resize_keyboard=True, input_field_placeholder='Выбери клиента')