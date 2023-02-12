from typing import Optional

from db.io.prints import error_print
from db.connection import connection


def insert_new_order(user_id, first_name, last_name, username, honey_id, honey_name, amount, total, place,
                     comment, order_date) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO orders
                    (user_id, first_name, last_name, username, honey_id, honey_name, amount, total, place, comment, order_date)
                    VALUES({user_id},'{first_name}', '{last_name}', '{username}', {honey_id}, '{honey_name}', {amount}, {total}, '{place}', '{comment}', '{order_date}');
            """

        )


def delete_order(order_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""delete from orders 
            where order_id = '{order_id}';
            """
        )

        result = cursor.fetchall()

        if len(result) == 0:
            error_print(f'no order with order_id: {order_id}')
            return False

        return True


def update_done_1(order_id) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE orders SET 
                done = 1
                WHERE orders.order_id = {order_id};
            """
        )


def is_user_has_new_order(user_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where orders.done = 0 and 
            orders.user_id = {user_id}
            """
        )
        result = cursor.fetchall()

        if len(result) == 0:
            return False

        return True


def is_user_has_changed_place_in_new_order(user_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where orders.done = 0 and 
            orders.user_id = {user_id} and
            place != 'none';
            """
        )
        result = cursor.fetchall()

        if len(result) == 0:
            return False

        return True

def get_all_orders() -> Optional[list]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where done = 1;
            """
        )

        result = cursor.fetchall()

        if len(result) == 0:
            error_print('no orders')
            return

        return result


def get_order(order_id) -> Optional[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where orders.order_id = {order_id};
            """
        )
        result = cursor.fetchall()

        if len(result) != 1:
            error_print(f'no order with {order_id}')
            return

        return result[0]


def get_new_user_order(user_id) -> Optional[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where orders.done = 0 and 
            orders.user_id = {user_id} and
            (orders.place = 'none' or
            orders.comment = 'none');
            """
        )
        result = cursor.fetchall()
        print(result)
        if len(result) != 1:
            error_print(f'User {user_id} has {len(result)} new orders, not 1')
            return

        return result[0]


def get_user_orders(user_id) -> Optional[list]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where done = 1 and user_id = '{user_id}';
            """
        )
        result = cursor.fetchall()

        if len(result) == 0:
            return

        return result


def get_all_done_orders() -> Optional[list]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where done = 2;
            """
        )

        result = cursor.fetchall()

        if len(result) == 0:
            return

        return result


def get_user_done_orders(user_id) -> Optional[list]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select * from orders
            where done = 2 and orders.user_id = '{user_id}';
            """
        )
        result = cursor.fetchall()

        if len(result) == 0:
            return

        return result


def set_place(order_id, place) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE orders SET 
                place = '{place}'
                WHERE orders.order_id = {order_id};
            """
        )


def set_comment(order_id, comment) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE orders SET 
                comment = '{comment}'
                WHERE orders.order_id = {order_id}
            """
        )
