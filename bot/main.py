import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup

from keyboard import get_all_preorders_menu
from config import bot_token, users
from utils.django_api import WebAppAPI

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def start(message: types.Message) -> None:
    if message.from_user.id in users:
        start_buttons = ["Предзаказы выгрузить", "Предазказы товара", "Добавить предзаказ", "Выгрузить предзаказы в Excel"]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer("Привет! Это база предзаказов! Чем помочь?", reply_markup=keyboard)
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


@dp.message_handler(Text(equals="Предзаказы выгрузить"))
async def get_preorders(message: types.Message) -> None:
    if message.from_user.id in users:
        preorders_menu = get_all_preorders_menu()
        await message.answer("Какие предзаказы выгрузить?", reply_markup=preorders_menu)
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('all_'))
async def inline_keyboard_preorders_buttons(callback: types.CallbackQuery) -> None:
    api = WebAppAPI("http://web-app:8000/api/v1")
    page_number = 1
    page_size = 10

    if callback.data == 'all_preorders':
        data = api.get_all_data("preorders", page_number=page_number, page_size=page_size)
    elif callback.data == 'all_active_preorders':
        data = api.get_all_data("preorders", page_number=page_number, page_size=page_size, bought=False, canceled=False)
    elif callback.data == 'all_bought_preorders':
        data = api.get_all_data("preorders", page_number=page_number, page_size=page_size, bought=True)
    elif callback.data == 'all_canceled_preorders':
        data = api.get_all_data("preorders", page_number=page_number, page_size=page_size, canceled=True)

    results = data['response_text']
    pages = data['pages']

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    page_buttons = [str(page_num) for page_num in range(1, pages + 1)]
    keyboard.add(*page_buttons)

    await callback.message.answer(results, reply_markup=keyboard)


@dp.message_handler(Text(equals='Выгрузить предзаказы в Excel'))
async def get_preorders_excel(message: types.Message) -> None:
    if message.from_user.id in users:
        api = WebAppAPI("http://web-app:8000/api/v1")
        file_csv = api.export_csv(endpoint='preorders')

        with open(file_csv, 'rb') as file:
            await bot.send_document(message.chat.id, file)

        if os.path.exists(file_csv):
            try:
                os.remove(file_csv)
            except OSError as ex:
                print(f"Ошибка при удалении файла: {ex}")
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


class Form(StatesGroup):
    number = State()
    product = State()
    color = State()
    size = State()
    quantity = State()
    price = State()
    city = State()
    shipping_adress = State()
    shipping_price = State()
    client_name = State()
    client_phone_number = State()
    type_of_connect = State()


@dp.message_handler(Text(equals='Добавить предзаказ'))
async def get_number(message: types.Message) -> None:
    if message.from_user.id in users:
        await Form.number.set()
        await message.reply('Введите номер заказа')
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    start_buttons = ["Предзаказы выгрузить", "Предазказы товара", "Добавить предзаказ", "Выгрузить предзаказы в Excel"]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await state.finish()
    await message.reply("Ок, всё отменяем.", reply_markup=keyboard)


@dp.message_handler(state=Form.number)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = int(message.text)

    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    list_products = ['Телогрейка', 'Жилетка', 'Пальто', 'Парка', 'Пальто зимнее', 'Шуба', 'Рубашка', 'Штаны', 'Пиждак']
    markup.add(*list_products)
    await message.reply('Какой товар? Выбери кнопкой.', reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ['Телогрейка', 'Жилетка', 'Пальто', 'Парка', 'Пальто зимнее',
                                                         'Шуба', 'Рубашка', 'Штаны', 'Пиждак'], state=Form.product)
async def process_product_invalid(message: types.Message):
    return await message.reply('Нужно выбрать товар кнопкой!')


@dp.message_handler(state=Form.product)
async def process_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product'] = message.text
    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    list_colors = ['Голубика', 'Облако', 'Розовый', 'Черный', 'Молочный', 'Кирпич', 'Горчица', 'Хаки']
    markup.add(*list_colors)
    await message.reply('Какой цвет? Выбери кнопкой.', reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ['Голубика', 'Облако', 'Розовый', 'Черный', 'Молочный',
                                                         'Кирпич', 'Горчица', 'Хаки'], state=Form.color)
async def process_color_invalid(message: types.Message):
    return await message.reply('Нужно выбрать цвет кнопкой!')


@dp.message_handler(state=Form.color)
async def process_color(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['color'] = message.text
    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    list_sizes = ['oversize', 'XS-S', 'S-M', 'M-L', 'мужской M-L']
    markup.add(*list_sizes)
    await message.reply('Какой размер? Выбери кнопкой.', reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ['oversize', 'XS-S', 'S-M', 'M-L', 'мужской M-L'],
                    state=Form.size)
async def process_size_invalid(message: types.Message) -> None:
    return await message.reply('Нужно выбрать размер кнопкой!')


@dp.message_handler(state=Form.size)
async def process_size(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['size'] = message.text
        markup = types.ReplyKeyboardRemove()
    await Form.next()
    await message.reply('Введите количество', reply_markup=markup)


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.quantity)
async def process_quantity(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['quantity'] = int(message.text)
    await Form.next()
    await message.reply('Введите цену.')


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.price)
async def process_price(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['price'] = int(message.text)
    await Form.next()
    await message.reply('Введите город для отправки.')


@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['city'] = message.text
    await Form.next()
    await message.reply('Введите адрес доставки.')


@dp.message_handler(state=Form.shipping_adress)
async def process_shipping_adress(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['shipping_adress'] = message.text
    await Form.next()
    await message.reply('Введите стоимость доставки.')


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.shipping_price)
async def process_shipping_price(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['shipping_price'] = int(message.text)
    await Form.next()
    await message.reply('Введите ФИО клиента')


@dp.message_handler(state=Form.client_name)
async def process_client_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['client_name'] = message.text
    await Form.next()
    await message.reply('Введите телефон клиента.')


@dp.message_handler(state=Form.client_phone_number)
async def process_client_phone_number(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['client_phone_number'] = message.text
    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    list_types_of_connect = ['WhatsApp', 'Telegram', 'Instagram', 'SMS', 'e-mail']
    markup.add(*list_types_of_connect)
    await message.reply('Выберите тип связи с клиентом.', reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ['WhatsApp', 'Telegram', 'Instagram', 'SMS', 'e-mail'],
                    state=Form.type_of_connect)
async def process_type_of_connect_invalid(message: types.Message):
    return await message.reply('Нужно выбрать тип связи кнопкой!')


@dp.message_handler(state=Form.type_of_connect)
async def process_type_of_connect(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type_of_connect'] = message.text

    start_buttons = ["Предзаказы выгрузить", "Предазказы товара", "Добавить предзаказ", "Выгрузить предзаказы в Excel"]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    data = await state.get_data()
    await state.finish()

    api = WebAppAPI("http://web-app:8000/api/v1")
    response = api.post_data('preorders', data)

    await message.reply(f'Запись успешно внесена! {response}', reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)