from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


mains = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = '/get_currencies'),
            KeyboardButton(text = '/convert')
        ],
        [
            KeyboardButton(text = 'админ-панель')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard= True,
    input_field_placeholder = 'Выберите действие из меню'

)
mains_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = '/manage_currency'),
            KeyboardButton(text = 'Назад')
        ],
        [
            KeyboardButton(text = '/get_currencies'),
            KeyboardButton(text = '/convert')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard= True,
    input_field_placeholder='Выберите действие из меню'
)
mains_func = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Добавить валюту'),
            KeyboardButton(text='Удалить валюту'),
            KeyboardButton(text="Изменить курс валюты"),

            KeyboardButton(text = 'Назад в админ-панель')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard= True,
    input_field_placeholder='Выберите действие из меню'
)

