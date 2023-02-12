from typing import Optional

from db.io.prints import system_print, error_print
from db.connection import connection


def create_new_honey(honey_id, price, capacity, amount, name, description, collected) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO honey_price
            (id, price, capacity, amount)
            VALUES({honey_id}, {price}, {capacity}, {amount});
            """
        )

        cursor.execute(
            f"""INSERT INTO honey_info
            (id, name, description, collected)
            VALUES({honey_id}, '{name}', '{description}', '{collected}');
            """
        )


def update_honey_price_table(honey_id, price, capacity, amount) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE honey_price SET 
                price = {price},
                capacity = {capacity},
                amount = {amount},
                WHERE honey_price.id = {honey_id};
            """
        )


def update_honey_info_table(honey_id, name, description, collected) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE honey_price SET 
                name = '{name}',
                description = '{description}',
                collected = '{collected}',
                WHERE honey_price.id = {honey_id};
            """
        )


def get_all_list_honey() -> list:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from honey_info;"""
        )
        res = cursor.fetchall()
        return res


def get_honey_info(honey_id) -> Optional[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from honey_info
                where honey_info.id ={honey_id};
            """
        )
        res = cursor.fetchall()
        if len(res) == 0:
            error_print(f"No honey with id: {honey_id}")
            return

        return res[0]


def get_honey_price(honey_id) -> Optional[int]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select price
                from honey_price 
                where honey_price.id = {honey_id};
            """
        )

        result = cursor.fetchall()

        if len(result) != 1:
            error_print(f"no honey with {honey_id} id")
            return

        return result[0][0]


def get_honey_amount(honey_id) -> Optional[int]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select amount
                from honey_price 
                where honey_price.id = {honey_id};
            """
        )

        result = cursor.fetchall()

        if len(result) != 1:
            error_print(f"no honey with {honey_id} id")
            return

        return result[0][0]


def buy_honey(user_id, user_balance, honey_id, amount_to_buy) -> str:  # enums
    error = ""
    honey_amount = get_honey_amount(honey_id)
    honey_price = get_honey_price(honey_id)

    if amount_to_buy > honey_amount:
        error = f"Жаль, но такого количества меда у нас нет :("
        return error

    if user_balance < amount_to_buy * honey_price:
        error = f"Не хватает средств, пополни кошелек"
        return error

    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE users_balance SET 
            balance = '{user_balance - amount_to_buy * honey_price}' 
            WHERE users_balance.id = '{user_id}';
            """
        )

        cursor.execute(
            f"""UPDATE honey_price SET 
            amount = {honey_amount - amount_to_buy} 
            WHERE honey_price.id = '{honey_id}';
            """
        )

        return 'success'

def insert_honey_amount(honey_id, amount) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE honey_price SET 
            amount = {amount} 
            WHERE id = '{honey_id}';
            """
        )

