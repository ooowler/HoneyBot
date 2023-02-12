from typing import Optional

from db.io.prints import system_print, error_print
from db.connection import connection


def create_new(user_id, honey_id, honey_amount) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO buying_transactions
            (user_id, honey_id, honey_amount)
            VALUES({user_id}, {honey_id}, {honey_amount});
            """
        )


def get_user_transaction_info(user_id) -> Optional[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select honey_id, honey_amount from buying_transactions
            where user_id = {user_id};
            """
        )

        result = cursor.fetchall()

        if len(result) == 0:
            return

        return result[0]


def is_user_exists(user_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from buying_transactions
            where user_id = {user_id};
            """
        )

        result = cursor.fetchall()

        if len(result) == 0:
            return False

        return True


def delete_transaction(user_id) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""DELETE FROM buying_transactions
                WHERE user_id = {user_id};
               """
        )
