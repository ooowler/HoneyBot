def dict_to_order_info(order: dict) -> str:
    '''
    keys:
    {'name', 'username', 'honey_id', 'amount', 'total', 'place', 'comment'}

    return:
    str, which can parse in HTML
    '''
    keys = ['name', 'username', 'honey_id', 'amount', 'total', 'place', 'comment']
    res: str = ''
    max_len_key = len(keys[0])
    offset = 2
    for key in keys:
        max_len_key = max(max_len_key, len(key))

    for key in keys:
        res += f'<code>{key}:{" " * (max_len_key - len(key) + offset)} | {order[key]} |</code>\n'

    return res


def str_to_products_info(price, amount, in_stock) -> str:
    '''
    products:
    ['Цена', 'Количество', 'В наличии']

    return:
    str, which can parse in HTML
    '''
    keys = {'Цена': f"{str(price)} рублей" , 'Количество': f"{str(amount)} грамм", 'В наличии': f"{in_stock} шт."}
    res: str = ''
    max_len_key = 0
    offset = 2
    for key in keys:
        max_len_key = max(max_len_key, len(key))

    for key in keys:
        res += f'<code>{key}:{" " * (max_len_key - len(key) + offset)} {keys[key]}</code>\n'

    return res
