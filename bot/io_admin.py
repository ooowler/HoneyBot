import db.query.orders as query_orders
from db.connection import connection
from bot.bot import bot
from system_info import admins


async def admin_send_message(message, reply_markup=None):
    for admin_id in admins:
        if reply_markup is not None:
            await bot.send_message(admin_id, message, reply_markup=reply_markup)
        else:
            await bot.send_message(admin_id, message)


def dict_to_order_info(order_id: int) -> str:
    '''
    keys:
    {order_id, user_id, first_name, last_name, username, honey_id, honey_name, amount, total, place, comment, order_date, done}

    return:
    str, which can parse in HTML
    '''
    order_items = query_orders.get_order(order_id)
    if order_items == -1:
        return "no order"

    items = ['order_id', 'user_id', 'first_name', 'last_name', 'username', 'honey_id', 'honey_name',
             'amount', 'total', 'place', 'comment', 'order_date', 'done']
    res: str = ''
    max_len_key = len(items[0])
    offset = 2
    for item in items:
        max_len_key = max(max_len_key, len(item))

    for i, order_item in enumerate(order_items):
        res += f'<code>{items[i]}:{" " * (max_len_key - len(items[i]) + offset)} | {order_item} |</code>\n'

    return res


def str_to_products_info(price, amount, in_stock) -> str:
    '''
    products:
    ['Цена', 'Количество', 'В наличии']

    return:
    str, which can parse in HTML
    '''
    keys = {'Цена': f"{str(price)} рублей", 'Количество': f"{str(amount)} грамм", 'В наличии': f"{in_stock} шт."}
    res: str = ''
    max_len_key = 0
    offset = 2
    for key in keys:
        max_len_key = max(max_len_key, len(key))

    for key in keys:
        res += f'<code>{key}:{" " * (max_len_key - len(key) + offset)} {keys[key]}</code>\n'

    return res
