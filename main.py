import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import crud_functions
import texts_bot
from config_bot import *
from keyboard_bot import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

crud_functions.initiate_db()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(texts_bot.start, reply_markup=start_kb)


@dp.message_handler(text=['О нас'])
async def about(message):
    await message.answer(texts_bot.about, reply_markup=start_kb)


@dp.message_handler(text=['Стоимость'])
async def info(message):
    await message.answer('Что вас интересует? ', reply_markup=catalog_kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    images = [
        'files/1.jpg',
        'files/2.jpg',
        'files/3.jpg',
        'files/4.jpg'
    ]
    items = crud_functions.get_all_products()
    if items:  # Проверка, не пустой ли список items
        for i, product in enumerate(items):
            if i < len(images):
                with open(images[i], 'rb') as img:
                    await message.answer_photo(img)
                    await message.answer(f'''Название: {product[1]} | 
                    Описание: {product[2]} | Цена: {product[3]}|
                    ''')
        await message.answer("Выберите продукт для покупки:", reply_markup=other_product)
    else:
        await message.answer("Список продуктов пуст.")


other_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')],
    ]
)


@dp.callback_query_handler(text='product_buying')
async def handle_product_buying(call):
    await send_confirm_message(call)


async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text='heart')
async def buy_heart(call):
    await call.message.answer(texts_bot.service_1, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='food')
async def buy_food(call):
    await call.message.answer(texts_bot.service_2, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='year')
async def buy_year(call):
    await call.message.answer(texts_bot.service_3, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='other')
async def buy_other(call):
    await call.message.answer(texts_bot.other, reply_markup=buy_kb)
    await call.answer()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='Регистрация')
async def sign_up(message):
    await message.answer('Введите имя пользователя (только латинские буквы)')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    is_inc = crud_functions.is_included(message.text)
    if is_inc is True:
        await message.answer('Данное имя уже занято, введите другое')
    else:
        await state.update_data(username=message.text)
        data = await state.get_data()
        await message.answer('Введите свой email')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_age(message, state):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer('Введите свой возраст')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def end_of_reg(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'])
    await state.finish()
    await message.answer('Благодарим за регистрацию на вашем балансе 1000 баллов',
                         reply_markup=start_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
