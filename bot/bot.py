from aiogram import Dispatcher, Bot
from system_info import TOKEN

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
