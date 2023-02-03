from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_main = [
    [
        types.KeyboardButton(text="Баланс"),
        types.KeyboardButton(text="Пополнить"),
        types.KeyboardButton(text="Купить мёд")
    ],
]
keyboard_main = types.ReplyKeyboardMarkup(
    keyboard=kb_main,
    resize_keyboard=True,
    input_field_placeholder="Выбери следующее действие",
)


kb_transaction = [
            [
                types.KeyboardButton(text="Подтвердить"),
                types.KeyboardButton(text="Отменить")
            ],
        ]

keyboard_transaction = types.ReplyKeyboardMarkup(
    keyboard=kb_transaction,
    resize_keyboard=True,
    input_field_placeholder="Выбери следующее действие",
)

inline_accept_1 = InlineKeyboardButton('Подтвердить оплату?', callback_data='pay_accept')
inline_cancel_2 = InlineKeyboardButton('Отменить оплату?', callback_data='pay_cancel')
inline_kb_transaction = InlineKeyboardMarkup().add(inline_accept_1, inline_cancel_2)