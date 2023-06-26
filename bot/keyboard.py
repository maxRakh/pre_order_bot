from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_all_preorders_menu():
    preorders_menu_keyboard = InlineKeyboardMarkup()
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Все предзаказы', callback_data='all_preorders'))
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Действующие', callback_data='all_active_preorders'))
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Выкупленные', callback_data='all_bought_preorders'))
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Отменённые', callback_data='all_canceled_preorders'))

    return preorders_menu_keyboard

