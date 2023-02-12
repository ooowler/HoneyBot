from typing import Optional

from db.io.prints import error_print
from db.connection import connection


def insert_user_balance_table(user_id, balance) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO
                users_balance(id, balance)
                VALUES({user_id}, {balance});
            """
        )


def insert_user_info_table(user_id, first_name, last_name, username) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO
                users_info(id, first_name, last_name, username)
                VALUES({user_id}, '{first_name}', '{last_name}', '{username}');
            """
        )


def get_user_balance(user_id) -> Optional[int]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select balance
                from users_balance 
                where users_balance.id = {user_id};
            """
        )

        result = cursor.fetchall()

        if len(result) != 1:
            error_print("invalid user balance fetch")
            return

        return result[0][0]


def get_user_info(user_id) -> Optional[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select *
                from users_info 
                where users_info.id = {user_id};
            """
        )

        result = cursor.fetchall()

        if len(result) != 1:
            error_print("invalid user info")
            return

        return result[0]


def check_user_exists(user_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select *
                from users_balance 
                where users_balance.id = {user_id};
            """
        )

        result = cursor.fetchall()

        if len(result) == 0:
            return False

        return True


def deposit(user_id, value) -> bool:
    user_balance = get_user_balance(user_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE users_balance SET 
                balance = '{user_balance + value}' 
                WHERE id = '{user_id}';
                """
            )

            return True
    except Exception as exc:
        error_print(f"NO DEPOSIT! {exc}")
        return False
