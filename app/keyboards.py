from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder , InlineKeyboardBuilder
from repo.db import all_item, Clients, Products


main = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text='Поставить тренировку в расписание')],
    [KeyboardButton(text='Добавить клиента'), KeyboardButton(text='Анкета ВПТ')],
    [KeyboardButton(text='Записать оплату')]
],
        resize_keyboard=True, 
        input_field_placeholder='Выбери пункт меню'
)

async def clients_kb():
    builder = InlineKeyboardBuilder()
    clients = {i.id: i.full_name for i in all_item(Clients) if i.status == 'inactive'}
    for client_id, full_name in clients.items():
        builder.button(text=full_name, callback_data=f'client:{client_id}')
    builder.button(text='Назад', callback_data='back')
    return builder.adjust(1).as_markup()

async def products_kb():
    builder = InlineKeyboardBuilder()
    products = [(i.id, i.name) for i in all_item(Products) if i.status == 'active']
    for id, name in products:
        builder.button(text=name, callback_data=f"product:{id}")
    builder.button(text='Назад', callback_data='back')   
    return builder.button(text='Назад', callback_data='back')
