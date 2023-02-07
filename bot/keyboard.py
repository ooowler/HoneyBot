from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_main = [
    [
        types.KeyboardButton(text="Баланс"),
        types.KeyboardButton(text="Пополнить"),
        types.KeyboardButton(text="Купить мёд"),
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

inline_accept_1 = InlineKeyboardButton('Подтвердить пополнение?', callback_data='deposit_accept')
inline_cancel_2 = InlineKeyboardButton('Отменить пополнение?', callback_data='deposit_cancel')
inline_kb_transaction = InlineKeyboardMarkup().add(inline_accept_1, inline_cancel_2)


class InlineHoney:
    __inline_kb_buy_honey_id_1 = InlineKeyboardMarkup().add(
        InlineKeyboardButton('1 шт', callback_data='buy_1_1'),
        InlineKeyboardButton('2 шт', callback_data='buy_1_2'),
        InlineKeyboardButton('3 шт', callback_data='buy_1_3'),
        InlineKeyboardButton('4 шт', callback_data='buy_1_4'),
        InlineKeyboardButton('5 шт', callback_data='buy_1_5'),
    )

    __inline_kb_buy_honey_id_2 = InlineKeyboardMarkup().add(
        InlineKeyboardButton('1 шт', callback_data='buy_2_1'),
        InlineKeyboardButton('2 шт', callback_data='buy_2_2'),
        InlineKeyboardButton('3 шт', callback_data='buy_2_3'),
        InlineKeyboardButton('4 шт', callback_data='buy_2_4'),
        InlineKeyboardButton('5 шт', callback_data='buy_2_5'),
    )

    __inline_kb_buy_honey_id_3 = InlineKeyboardMarkup().add(
        InlineKeyboardButton('1 шт', callback_data='buy_3_1'),
        InlineKeyboardButton('2 шт', callback_data='buy_3_2'),
        InlineKeyboardButton('3 шт', callback_data='buy_3_3'),
        InlineKeyboardButton('4 шт', callback_data='buy_3_4'),
        InlineKeyboardButton('5 шт', callback_data='buy_3_5'),
    )

    __all_inline_honey = {1: __inline_kb_buy_honey_id_1, 2: __inline_kb_buy_honey_id_2, 3: __inline_kb_buy_honey_id_3}

    def get_list_inline_honey(self):
        return self.__all_inline_honey


inline_list = InlineHoney()


inline_accept_1 = InlineKeyboardButton('Верно?', callback_data='pay_accept')
inline_cancel_2 = InlineKeyboardButton('Отмена?', callback_data='pay_cancel')
pay_keyboard = InlineKeyboardMarkup().add(inline_accept_1, inline_cancel_2)


choose_place_1 = InlineKeyboardButton('Альпийский переулок, 15к2', callback_data='dorm_itmo')
choose_place_2 = InlineKeyboardButton('Площадь Стачек, 5', callback_data='dorm_gum')
choose_place = InlineKeyboardMarkup().add(choose_place_1, choose_place_2)


