from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_all_preorders_menu():
    preorders_menu_keyboard = InlineKeyboardMarkup()
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Все предзаказы', callback_data='all_preorders'))
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Действующие', callback_data='all_active_preorders'))
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Выкупленные', callback_data='all_bought_preorders'))
    preorders_menu_keyboard.insert(InlineKeyboardButton(text='Отменённые', callback_data='all_canceled_preorders'))

    return preorders_menu_keyboard


def get_selected_product_preorders_menu():
    product_selected_preorders_menu = InlineKeyboardMarkup()
    list_products = ['Телогрейка', 'Жилетка', 'Пальто', 'Парка', 'Пальто зимнее', 'Шуба', 'Рубашка', 'Штаны', 'Пиждак']

    for product in list_products:
        product_selected_preorders_menu.insert(InlineKeyboardButton(text=product, callback_data=f'select_{product}'))

    return product_selected_preorders_menu