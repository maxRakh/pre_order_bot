import csv
import io
import os
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup

from keyboard import get_all_preorders_menu
from config import bot_token, users
from utils.django_api import WebAppAPI

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot)


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

        try:
            os.remove(file_csv)
        except OSError as ex:
            print(f"Ошибка при удалении файла: {ex}")
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


# @dp.message_handler(Text(equals=))# ИЗМЕНИТЬ
# async def get_all_preorders(message: types.Message) -> None:
#     if message.from_user.id in users:
#         api = WebAppAPI("http://web-app:8000/api/v1")
#         page_number = 1
#         page_size = 10
#
#         data = api.get_all_data("preorder", page_number=page_number, page_size=page_size)
#
#         results = data['response_text']
#         count = data['count']
#         pages = data['pages']
#         keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#         page_buttons = [str(page_num) for page_num in range(1, pages + 1)]
#         keyboard.add(*page_buttons)
#
#         await message.answer(results, reply_markup=keyboard)
#     else:
#         await message.answer("Извините, но у вас нет доступа к боту.")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)