from datetime import datetime
from loguru import logger
from aiogram import types, executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from bot.io_admin import dict_to_order_info, str_to_products_info
from system_info import PAYMENTS_TOKEN, admins
from bot.bot import bot, dp
from bot.io_admin import admin_send_message
from bot.keyboard import inline_honey_list

import db.query.create_tables as query_create_tables
import db.query.honey as query_honey
import db.query.orders as query_orders
import db.query.users as query_users
import db.query.buying_transactions as query_buying_transactions
import bot.keyboard as kb
import re

query_create_tables.to_create_all_tables()


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    user_exist = query_users.check_user_exists(message.chat.id)
    if user_exist:
        if message.chat.id in admins:
            await bot.send_message(message.chat.id, "Привет мой господин\nтебе доступна команда: <code>/admin</code>",
                                   reply_markup=kb.keyboard_main)
        else:
            await bot.send_message(message.chat.id, "Привет! Я тебя помню :)", reply_markup=kb.keyboard_main)
    else:
        query_users.insert_user_balance_table(message.chat.id, 0)
        query_users.insert_user_info_table(message.chat.id, message.chat.first_name, message.chat.last_name,
                                           message.chat.username)
        await bot.send_message(message.chat.id, "Привет!", reply_markup=kb.keyboard_main)


@dp.message_handler(commands=['admin'])
async def begin(message: types.Message):
    user_id = message.chat.id
    if user_id not in admins:
        return

    commands: str = '<code>orders_list_[0, 1, 2, 3]</code>\n' \
                    '<code>admin_msg [your message]</code>\n' \
                    '<code>insert_honey_[honey_id]_[honey_amount]</code>\n' \
                    '<code>get_honey_amount_[honey_id]</code>' \
                    ''
    await bot.send_message(user_id, commands)


@dp.message_handler(text="Баланс")
async def get_balance(message: types.Message):
    balance = query_users.get_user_balance(message.chat.id)
    if balance:
        await message.reply(f"Твой баланс: {balance}")
    else:
        await message.reply(f"Возникла ошибка, напишите в поддержку или попробуйте: <code>/start</code>")


@dp.message_handler(text="Пополнить")
async def deposit(message: types.Message):
    await bot.send_message(message.chat.id, "Введи сумму к пополнению")


@dp.message_handler(lambda msg: msg.text.isdigit() and int(msg.text) > 0)
async def depo_sum(message: types.Message):
    num = int(message.text)
    if num < 60:
        await bot.send_message(message.chat.id, "Пополни от 60 рублей", reply_markup=kb.keyboard_main)
        return
    if num > 3000:
        await bot.send_message(message.chat.id, "Куда тебе столько меда?", reply_markup=kb.keyboard_main)
        return

    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Тестовый платеж!')

    PRICE = types.LabeledPrice(label=f'К оплате: {num} рублей', amount=num * 100)  # 1 руб = 100 копеек
    await bot.send_invoice(message.chat.id,
                           title='Вкусный мёд',
                           description='Пополни и Купи ↑',
                           provider_token=PAYMENTS_TOKEN,
                           currency='rub',
                           photo_url='https://media.istockphoto.com/id/520733611/photo/jar-of-honey-with-honeycomb.jpg?s=612x612&w=0&k=20&c=k7s6XnJvM1O3kLfy5XUn1M169j11Zcca9rFgvIBGkUE=',
                           photo_width=800,
                           photo_height=612,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter='depo_for_honey',
                           payload='test_payload')


# pre checkout (must be answered in 10 seconds)

@dp.pre_checkout_query_handler(lambda pay_query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    user_id = message.chat.id
    total_rub = message.successful_payment.total_amount // 100
    res = query_users.deposit(user_id, total_rub)
    if res:
        await bot.send_message(message.chat.id, f'Баланс пополнен на сумму: {total_rub} рублей!')
    else:
        await admin_send_message(
            f"[ALERT!]\nДеньги отправлены, но БД не записала\nuser_id: {user_id}, username:{message.chat.username}, amount: {total_rub} рублей!")
        await bot.send_message(message.chat.id,
                               f"Просим прощения, возникла ошибка\nМы получили уведомление, решаем проблему\n")


@dp.message_handler(text="Купить мёд")
async def buy(message: types.Message):
    honey_list = query_honey.get_all_list_honey()
    user_id = message.chat.id
    if query_orders.is_user_has_new_order(user_id):
        if query_orders.is_user_has_changed_place_in_new_order(user_id):
            await bot.send_message(user_id, 'Пожалуйста, напиши комментарий к прошлому заказу',
                                   reply_markup=types.ReplyKeyboardRemove())
        else:
            await bot.send_message(user_id, 'Пожалуйста, выбери место получелния к прошлому заказу',
                                   reply_markup=types.ReplyKeyboardRemove())
        return

    await bot.send_message(user_id, "<b>Список товаров</b>", reply_markup=kb.keyboard_main)
    for honey in honey_list:
        amount = query_honey.get_honey_amount(honey[0])
        price = query_honey.get_honey_price(honey[0])
        if not amount:
            continue

        product_info = str_to_products_info(price, 200, amount)
        info_to_user = f"""<b>Мёд {honey[1]}</b> 🍯\n\n<b>Описание</b>\n{honey[2]}\n\n<b>Собран</b>\n{honey[3]}\n\n<code>{product_info}</code>"""
        await bot.send_message(message.chat.id, info_to_user, reply_markup=inline_honey_list[honey[0]])


@dp.callback_query_handler(Text(startswith="buy_"))
async def buy_callback(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    if query_buying_transactions.is_user_exists(user_id):
        await bot.send_message(user_id, 'Пожалуйста, заверши оформление прошлой покупки')
        return

    honey_id = int(callback_query.data[-3])
    honey_amount = int(callback_query.data[-1])
    honey_price = query_honey.get_honey_price(honey_id)
    honey_info = query_honey.get_honey_info(honey_id)
    query_buying_transactions.create_new(user_id, honey_id, honey_amount)
    await bot.send_message(user_id,
                           f"Ты выбрал {honey_info[1]} мёд на сумму: {honey_amount * honey_price} рублей\nПрекрасный выбор!",
                           reply_markup=kb.pay_keyboard)


@dp.callback_query_handler(text="pay_accept")
async def pay_accept(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    await bot.delete_message(user_id, callback_query.message.message_id)

    if not query_buying_transactions.is_user_exists(user_id):
        await bot.send_message(user_id, 'Товар не выбран')
        return

    user_info = query_users.get_user_info(user_id)

    user_balance = query_users.get_user_balance(user_id)
    user_transaction_info = query_buying_transactions.get_user_transaction_info(user_id)
    honey_id = user_transaction_info[0]
    honey_amount = user_transaction_info[1]
    honey_price = query_honey.get_honey_price(honey_id)
    honey = query_honey.get_honey_info(honey_id)
    total = honey_amount * honey_price

    res = query_honey.buy_honey(user_id, user_balance, honey_id, honey_amount)
    if res != 'success':
        query_buying_transactions.delete_transaction(user_id)
        await bot.send_message(user_id, res)
        return

    await admin_send_message(
        f"[ADMIN] {user_id} купил мед под id: {honey_id} в количестве {honey_amount} шт")

    time_order = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query_orders.insert_new_order(user_id, user_info[1], user_info[2], user_info[3], honey_id, honey[1],
                                  honey_amount, total, "none", "none", time_order)

    await bot.send_message(user_id,
                           f"Ты купил {honey[1]} мёд на {honey_amount * honey_price} рублей! Выбери место получения",
                           reply_markup=kb.choose_place)


@dp.callback_query_handler(text="pay_cancel")
async def pay_cancel(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    await bot.delete_message(user_id, callback_query.message.message_id)

    if not query_buying_transactions.is_user_exists(user_id):
        await bot.send_message(user_id, 'Товар не выбран')
        return

    query_buying_transactions.delete_transaction(user_id)
    await bot.send_message(user_id, "Отменено!")


@dp.callback_query_handler(Text(startswith="dorm_"))
async def buy_callback(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    if not query_buying_transactions.is_user_exists(user_id):
        await bot.send_message(user_id, 'Товар не выбран')
        return

    dorm = callback_query.data[5]
    if query_orders.is_user_has_new_order(user_id) and query_orders.is_user_has_changed_place_in_new_order(user_id):
        await bot.send_message(user_id, 'Пожалуйста, введи комментарий', reply_markup=types.ReplyKeyboardRemove())
        return

    order = query_orders.get_new_user_order(user_id)
    order = order[0]
    dorm_to_string = "Альпийский переулок, 15к2" if dorm == "i" else "Площадь Стачек, 5"
    query_orders.set_place(order, dorm_to_string)
    await bot.delete_message(user_id, callback_query.message.message_id)

    await bot.send_message(user_id,
                           f"Отлично! Напиши комментарий к заказу",
                           reply_markup=types.ReplyKeyboardRemove())


# ---- ADMIN COMMANDS ----


@dp.message_handler(Text(startswith="admin_msg"))
async def admin_msg(message: types.Message):
    if message.chat.id in admins:
        for admin_id in admins:
            if admin_id == message.chat.id:
                await bot.send_message(admin_id, 'Отправлено!')
                continue

            text = message.text.replace('admin_msg', '')

            if len(text) != 0:
                await bot.send_message(admin_id, f'[ADMIN MESSAGE] {text}')


@dp.message_handler(Text(startswith="insert_honey_"))
async def admin_msg(message: types.Message):
    user_id = message.chat.id
    if user_id in admins:
        if len(message.text.split('_')) != 4:
            await bot.send_message(user_id, 'Invalid query. Incorrect args')
            return

        honey_id = message.text.split('_')[2]
        honey_amount = message.text.split('_')[3]

        if not (honey_amount.isdigit() and honey_amount.isdigit()):
            await bot.send_message(user_id, 'please, enter a number')
            return

        query_honey.insert_honey_amount(honey_id, honey_amount)
        await bot.send_message(user_id, 'Maybe success, verify honey amount')


@dp.message_handler(Text(startswith="get_honey_amount_"))
async def admin_msg(message: types.Message):
    user_id = message.chat.id
    if user_id in admins:
        if len(message.text.split('_')) != 4:
            await bot.send_message(user_id, 'Invalid query. Incorrect args')
            return

        honey_id = message.text.split('_')[3]
        if not honey_id.isdigit():
            await bot.send_message(user_id, 'please, enter a number')
            return

        honey_amount = query_honey.get_honey_amount(honey_id)

        if honey_amount:
            await bot.send_message(user_id, f'honey_amount: {honey_amount}')
        else:
            await bot.send_message(user_id, f'no honey with id: {honey_id}')


@dp.message_handler(Text(startswith="orders_list_"))
async def admin_order_list_info(message: types.Message):
    user_id = message.chat.id
    if user_id in admins:
        done_id = int(message.text[-1])
        if done_id not in [0, 1, 2, 3]:
            await bot.send_message(user_id, 'only [0, 1, 2, 3] states can be')
            return
        orders = query_orders.get_all_orders_done_id(done_id)
        if not orders:
            await bot.send_message(user_id, 'no orders')
            return

        for order in orders:
            msg = dict_to_order_info(order[0])
            if done_id == 0:
                await bot.send_message(user_id, f"[PENDING PAYMENT ORDERS]\n\n{msg}")
            if done_id == 1:
                await bot.send_message(user_id, f"[PAID ORDERS]\n\n{msg}",
                                       reply_markup=kb.admin_keyboard_order_complete)
            elif done_id == 2:
                await bot.send_message(user_id, f"[COMPLETED ORDERS]\n\n{msg}")

            elif done_id == 3:
                await bot.send_message(user_id, f"[CANCELED ORDERS]\n\n{msg}")


@dp.callback_query_handler(text="order_complete")
async def order_complete(callback_query: types.CallbackQuery):
    user_id = callback_query["from"]["id"]
    order_id_start_index = re.search("\d", callback_query.message.text).start()
    order_id_end_index = order_id_start_index
    while callback_query.message.text[order_id_end_index].isdigit():
        order_id_end_index += 1

    order_id_num = int(callback_query.message.text[order_id_start_index: order_id_end_index])

    query_orders.update_done_2(order_id_num)
    await bot.delete_message(user_id, callback_query.message.message_id)


# ---- DEFAULT -----
@dp.message_handler()
async def default_func(message: types.Message):
    user_id = message.chat.id
    if not query_buying_transactions.is_user_exists(user_id):
        return

    new_order = query_orders.get_new_user_order(user_id)
    if new_order:
        order_id = new_order[0]
        if len(message.text) > 70:
            await bot.send_message(user_id, f"Я думаю, комментарий должен быть поменьше, введи еще раз")
            return

        if not query_orders.is_user_has_changed_place_in_new_order(user_id):
            await bot.send_message(user_id, 'Пожалуйста, выбери место получения к прошлому заказу',
                                   reply_markup=types.ReplyKeyboardRemove())
            return

        query_orders.set_comment(order_id, message.text)
        query_orders.update_done_1(order_id)
        query_buying_transactions.delete_transaction(user_id)

        msg = dict_to_order_info(order_id)
        await admin_send_message(f"<b>[ORDER]</b>\n\n{msg}",
                                 reply_markup=kb.keyboard_main)

        await bot.send_message(user_id,
                               f"Заказ принят на сумму {new_order[8]} рублей\nМожно забрать в {new_order[9]}\nТвой комментарий: {message.text}",
                               reply_markup=kb.keyboard_main)


executor.start_polling(dp)
