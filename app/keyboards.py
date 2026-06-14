from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder , InlineKeyboardBuilder
from repo.db import all_item, Clients, Products


main = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text='Записть посещение')],
    [KeyboardButton(text='Записать оплату')], 
    [KeyboardButton(text='Добавить клиента'), KeyboardButton(text='Анкета ВПТ')]
],
        resize_keyboard=True, 
        input_field_placeholder='Выбери пункт меню'
)

async def clients_kb():
    builder = InlineKeyboardBuilder()
    clients = [(i.id, i.full_name) for i in all_item(Clients) if i.status == 'new']
    for client_id, full_name in clients:
        builder.button(text=full_name, callback_data=f'client:{client_id}')
    builder.button(text='Назад', callback_data='back')
    return builder.adjust(1).as_markup()

async def hot_clients():
    builder = InlineKeyboardBuilder()
    clients = [(i.id, i.full_name) for i in all_item(Clients)  if i.status != 'churn']
    for client_id, full_name in clients:
        builder.button(text=full_name, callback_data=f'client:{client_id}')
    builder.button(text='Назад', callback_data='back')
    return builder.adjust(1).as_markup()

async def products_kb():
    builder = InlineKeyboardBuilder()
    products = [(i.id, i.name) for i in all_item(Products) if i.status == 'active']
    for id, name in products:
        builder.button(text=name, callback_data=f"product:{id}")
    builder.button(text='Назад', callback_data='back')   
    return builder.adjust(1).as_markup()

async def true_false():
    builder = InlineKeyboardBuilder()
    for res, text in [(True, 'Да'), (False, 'Нет')]:
        builder.button(text=text, callback_data=res)
    builder.button(text='Назад', callback_data='back')
    return builder.adjust(1).as_markup()
