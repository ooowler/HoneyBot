from aiogram import types, executor, Dispatcher, Bot

token_file = open('token')
TOKEN = token_file.readline()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, "Привет, мир!")


executor.start_polling(dp)