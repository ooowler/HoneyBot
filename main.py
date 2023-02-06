import psycopg2
from loguru import logger
from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.honey_info import honey
import db.honey_info as honey_info

from db.connection import connect_to_db, close_db
import db.query as query
import bot.keyboard as kb
from db.config import host, user, password, db_name, port
from db.io.prints import system_print, error_print

token_file = open('token')
TOKEN = token_file.readline()

admin_file = open('admin')
admin_id = int(admin_file.readline())

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

connection = connect_to_db()

deposit_transactions = dict()
buying_transactions = dict()
order_list = dict()
all_honey = honey.get_all_honey()
inline_honey_list = kb.inline_list.get_list_inline_honey()


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    logger.info(message)
    user_exist = query.check_user_exist(connection, message.chat.id)
    if user_exist:
        await bot.send_message(message.chat.id, "Снова привет!", reply_markup=kb.keyboard_main)
    else:
        query.insert_to_user_table(connection, message.chat.id, 0)
        await bot.send_message(message.chat.id, "Привет!", reply_markup=kb.keyboard_main)


@dp.message_handler(text="Домой")
async def begin(message: types.Message):
    user_exist = query.check_user_exist(connection, message.chat.id)
    if user_exist:
        await bot.send_message(message.chat.id, "Снова привет!", reply_markup=kb.keyboard_main)
    else:
        query.insert_to_user_table(connection, message.chat.id, 0)
        await bot.send_message(message.chat.id, "Привет!", reply_markup=kb.keyboard_main)


@dp.message_handler(text="Баланс")
async def get_balance(message: types.Message):
    balance = query.get_user_balance(connection, message.chat.id)
    if balance == -1:
        await message.reply(f"Возникла ошибка, напишите в поддержку")
    else:
        await message.reply(f"Твой баланс: {balance}")


@dp.message_handler(text="Пополнить")
async def deposit(message: types.Message):
    await bot.send_message(message.chat.id, "Введи сумму к пополнению")


@dp.message_handler(lambda msg: msg.text.isdigit() and int(msg.text) > 0)
async def depo_sum(message: types.Message):
    num = int(message.text)
    if num > 3000:
        await bot.send_message(message.chat.id, "Куда тебе столько меда?", reply_markup=kb.keyboard_main)
        return

    if message.chat.id in deposit_transactions:
        await bot.send_message(message.chat.id,
                               f"Подтверди или отмени пополнение на сумму {deposit_transactions[message.chat.id]} рублей",
                               reply_markup=kb.keyboard_transaction)
        return
    deposit_transactions[message.chat.id] = num
    await bot.send_message(message.chat.id, "Пополни и нажми кнопку подтвердить\nреквизиты: 4276060066934898 (сбер)",
                           reply_markup=kb.keyboard_transaction)


@dp.message_handler(text="Подтвердить")
async def deposit_accept(message: types.Message):
    await bot.send_message(message.chat.id, "Мы проверяем платеж, скоро ответим!", reply_markup=kb.keyboard_main)
    user_id = message.chat.id
    if user_id in deposit_transactions:
        await bot.send_message(admin_id, f"[ADMIN] {message.chat.id} отправляет {deposit_transactions[user_id]} рублей",
                               reply_markup=kb.inline_kb_transaction)
    else:
        error_print("такой транзакции нет")


@dp.message_handler(text="Отменить")
async def deposit_cancel(message: types.Message):
    await bot.send_message(message.chat.id, "Заказ отменен!", reply_markup=kb.keyboard_main)
    user_id = message.chat.id
    if user_id in deposit_transactions:
        await bot.send_message(admin_id,
                               f"[ADMIN] {message.chat.id} отменил заказ на {deposit_transactions[user_id]} рублей")
        del deposit_transactions[user_id]
    else:
        error_print("такой транзакции нет")


@dp.callback_query_handler(text="deposit_accept")
async def deposit_accept_admin(callback_query: types.CallbackQuery):
    # user_id = callback_query["from"]["id"]
    user_id = callback_query.message.text[8:8 + 8 + 1]  # warning!
    user_id = int(user_id)
    if user_id not in deposit_transactions:
        return

    if user_id in deposit_transactions:
        query.deposit(connection, user_id, deposit_transactions[user_id])
        await bot.send_message(admin_id,
                               f"[ADMIN] {user_id} пополнение ПОДТВЕРЖДЕНО на сумму {deposit_transactions[user_id]} рублей")
        del deposit_transactions[user_id]
        await bot.send_message(user_id, "Баланс пополнен!")


@dp.callback_query_handler(text="deposit_cancel")
async def deposit_cancel_admin(callback_query: types.CallbackQuery):
    user_id = int(callback_query.message.text[8:8 + 8 + 1])  # warning!
    if user_id not in deposit_transactions:
        return

    await bot.send_message(admin_id,
                           f"[ADMIN] {user_id} пополнение ОТМЕНЕНО на сумму {deposit_transactions[user_id]} рублей")
    await bot.send_message(user_id, "Транзакция отменена!")
    del deposit_transactions[user_id]


@dp.message_handler(text="Купить мёд")
async def buy(message: types.Message):
    await bot.send_message(message.chat.id, "cписок товаров", reply_markup=kb.keyboard_main)
    for honey_key in all_honey.keys():
        amount = query.get_honey_amount(connection, honey_key)
        info_to_user = f"""Мёд: {all_honey[honey_key]["name"]}\n{all_honey[honey_key]["info"]}\nцена: {all_honey[honey_key]["price"]}рублей / 200 грамм\nв наличие: {amount} штук"""
        await bot.send_message(message.chat.id, info_to_user, reply_markup=inline_honey_list[honey_key])


@dp.callback_query_handler(Text(startswith="buy_"))
async def buy_callback(callback_query: types.CallbackQuery):
    honey_id = int(callback_query.data[-3])
    honey_amount = int(callback_query.data[-1])
    user_id = callback_query["from"]["id"]
    buying_transactions[user_id] = {"honey_id": honey_id, "honey_amount": honey_amount}
    await bot.send_message(user_id,
                           f"Ты выбрал мёд под номером {honey_id} в количестве {honey_amount} штук\nПрекрасный выбор!",
                           reply_markup=kb.pay_keyboard)


@dp.callback_query_handler(Text(startswith="dorm_"))
async def buy_callback(callback_query: types.CallbackQuery):
    dorm = callback_query.data[5]
    user_id = callback_query["from"]["id"]
    dorm_to_string = "Общежитие №3 ИТМО" if dorm == "i" else "Общежитие ГУМ РФ"
    await bot.send_message(user_id,
                           f"Заказ принят, можно забрать в {dorm_to_string}",
                           reply_markup=kb.keyboard_main)
    order_list[user_id]["place"] = dorm_to_string
    await bot.send_message(admin_id,
                           f"[ORDER!]\n{order_list[user_id]}",
                           reply_markup=kb.keyboard_main)
    del order_list[user_id]


@dp.callback_query_handler(text="pay_accept")
async def pay_accept(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    if user_id not in buying_transactions:
        error_print("Заказа не было создано!")
        await bot.send_message(user_id, "Ты не сделал заказ")
        return

    honey_id = buying_transactions[user_id]["honey_id"]
    honey_amount = buying_transactions[user_id]["honey_amount"]
    honey_price = query.get_honey_price(connection, honey_id)

    res = query.buy_honey(connection, user_id, honey_id, honey_amount)
    if res is not True:
        del buying_transactions[user_id]
        await bot.send_message(user_id, res)
        return

    await bot.send_message(admin_id,
                           f"[ADMIN] {user_id} купил мед под id: {honey_id} в количестве {honey_amount} шт")
    order_list[user_id] = {"name": callback_query["from"]["first_name"], "username": callback_query["from"]["username"],
                           "honey_id": honey_id, "amount": honey_amount,
                           "total": honey_amount * honey_price,
                           "place": "none"}


    del buying_transactions[user_id]
    await bot.send_message(user_id, f"Куплено на {honey_amount * honey_price} рублей! Выбери место получения",
                           reply_markup=kb.choose_place)


@dp.callback_query_handler(text="pay_cancel")
async def pay_cancel(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    if user_id not in buying_transactions:
        error_print("Заказа не было создано!")
        await bot.send_message(user_id, "Ты уже отменил заказ")
        return

    del buying_transactions[user_id]
    await bot.send_message(user_id, "Отменено!")


@dp.message_handler(text="order_list_info")
async def default_func(message: types.Message):
    print(order_list)


@dp.message_handler()
async def default_func(message: types.Message):
    await bot.send_message(message.chat.id, "Я не понял")


executor.start_polling(dp)
