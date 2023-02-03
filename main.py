import psycopg2
from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

transactions = dict()


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    user_exist = query.check_user_exist(connection, message.chat.id)
    if user_exist:
        await bot.send_message(message.chat.id, "Снова привет!", reply_markup=kb.keyboard_main)
    else:
        query.insert_to_user_table(connection, message.chat.id, 0)
        await bot.send_message(message.chat.id, "Привет!", reply_markup=kb.keyboard_main)


@dp.message_handler(text="домой")
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


@dp.message_handler(text="Подтвердить")
async def deposit(message: types.Message):
    await bot.send_message(message.chat.id, "Мы проверяем платеж, скоро ответим!", reply_markup=kb.keyboard_main)
    user_id = message.chat.id
    if user_id in transactions:
        await bot.send_message(admin_id, f"[ADMIN] {message.chat.id} отправляет {transactions[message.chat.id]} рублей",
                               reply_markup=kb.inline_kb_transaction)
    else:
        error_print("такой транзакции нет")


@dp.callback_query_handler(text="pay_accept")
async def transaction(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    if user_id in transactions:
        query.deposit(connection, user_id, transactions[user_id])
        del transactions[user_id]
        await bot.send_message(callback_query["from"]["id"], "баланс пополнен!")
    else:
        await bot.send_message(callback_query["from"]["id"], "произошла ошибка")
        error_print("заказ не был создан")


@dp.callback_query_handler(text="pay_cancel")
async def transaction(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query["from"]["id"], "транзакция отменена!")
    user_id = callback_query["from"]["id"]
    if user_id in transactions:
        del transactions[user_id]


@dp.message_handler()
async def deposit(message: types.Message):
    num = message.text
    if num.isdigit() and int(num) > 0:

        transactions[message.chat.id] = int(num)
        await bot.send_message(message.chat.id, "Пополни в течение 15 минут и нажми кнопку подтвердить",
                               reply_markup=kb.keyboard_transaction)

    else:
        await bot.send_message(message.chat.id, "Введи сумму правильно!", reply_markup=kb.keyboard_main)


executor.start_polling(dp)
