import psycopg2
from aiogram import types, executor, Dispatcher, Bot
from db.connection import connect_to_db, close_db
from db.query import create_table
from db.config import host, user, password, db_name, port
from db.io.prints import system_print

token_file = open('token')
TOKEN = token_file.readline()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

connection = connect_to_db()

@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, "Привет, мир!")


executor.start_polling(dp)
