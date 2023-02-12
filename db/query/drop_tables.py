from db.io.prints import system_print, error_print
from db.connection import connection


def delete_table_users_info() -> None:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users_info;")


def delete_table_users_balance() -> None:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users_balance;")


def delete_table_honey_info() -> None:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS honey_info;")


def delete_table_honey_price() -> None:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS honey_price;")


def delete_table_orders() -> None:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS orders;")


def delete_table_buying_transactions() -> None:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS buying_transactions;")
