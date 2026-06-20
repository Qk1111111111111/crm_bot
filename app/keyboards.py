from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder , InlineKeyboardBuilder
from repo.db import all_item, Clients, Products


main = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text='📅Записать посещение'), KeyboardButton(text='💳Записать оплату')], 
    [KeyboardButton(text='👤Добавить клиента'), KeyboardButton(text='📝Анкета ВПТ')]
],
        resize_keyboard=True, 
        input_field_placeholder='Выбери пункт меню'
)

async def clients_kb():
    builder = InlineKeyboardBuilder()
    clients = [(i.id, i.full_name) for i in all_item(Clients) if i.status != 'inactive']
    for client_id, full_name in clients:
        builder.button(text=full_name, callback_data=f'client:{client_id}')
    builder.button(text='Назад', callback_data='back')
    return builder.adjust(1).as_markup()


# async def clients_kb_hot():
#     builder = InlineKeyboardBuilder()
#     clients = [(i.id, i.full_name) for i in all_item(Clients)  if i.status != 'churn']
#     for client_id, full_name in clients:
#         builder.button(text=full_name, callback_data=f'client_hot:{client_id}')
#     builder.button(text='Назад', callback_data='back')
#     return builder.adjust(1).as_markup()

async def products_kb():
    builder = InlineKeyboardBuilder()
    products = [(i.id, i.description) for i in all_item(Products) if i.status == 'active']
    for id, description in products:
        builder.button(text=description, callback_data=f"product:{id}")
    builder.button(text='Назад', callback_data='back')   
    return builder.adjust(1).as_markup()


async def true_false():
    builder = InlineKeyboardBuilder()

    builder.button(text='Да', callback_data='visit:attended:true')
    builder.button(text='Нет', callback_data='visit:attended:false')

    builder.button(text='Назад', callback_data='back')
    return builder.adjust(2).as_markup()

