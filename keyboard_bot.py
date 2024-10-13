from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Стоимость'),
            KeyboardButton(text='О нас'),
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Регистрация'), #добавляем кнопки на главном меню
        ]
    ], resize_keyboard=True
)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Кардиология', callback_data='heart')],
        [InlineKeyboardButton(text='Нутрициология', callback_data='food')],
        [InlineKeyboardButton(text='Сопровождение', callback_data='year')],
        [InlineKeyboardButton(text='Другие предложения', callback_data='other')],
    ]
)



buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Купить', url='https://nutricardio.ru/')]
    ]
)