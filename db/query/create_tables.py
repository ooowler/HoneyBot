from db.io.prints import system_print, error_print
from db.connection import connection


def create_table_users_info() -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS users_info
            (
                id int UNIQUE,
                first_name varchar(50) NOT NULL,
                last_name varchar(50) NOT NULL,
                username varchar(50) NOT NULL
            );
            """
        )

        system_print("Users_info table created successfully")


def create_table_users_balance() -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS users_balance (
                 id int UNIQUE,
                 balance int NOT NULL
            );
            """
        )

        system_print("Users_balance table created successfully")


def create_table_honey_info() -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS honey_info (
                 id int UNIQUE,
                 name varchar(50) NOT NULL,
                 description varchar(200) NOT NULL,
                 collected varchar(100) NOT NULL
            );
            """
        )

        system_print("Honey_info table created successfully")


def create_table_honey_price() -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS honey_price (
                 id int UNIQUE,
                 price int NOT NULL,
                 capacity int NOT NULL,
                 amount int NOT NULL
            );
            """
        )

        system_print("Honey_price table created successfully")


def create_table_orders() -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS orders (
                 order_id serial PRIMARY KEY,
                 user_id int NOT NULL,
                 first_name varchar(50) NOT NULL,
                 last_name varchar(50) NOT NULL,
                 username varchar(50) NOT NULL,
                 honey_id int NOT NULL,
                 honey_name varchar(50) NOT NULL,
                 amount int NOT NULL,
                 total int NOT NULL,
                 place varchar(50) NOT NULL,
                 comment varchar(50),
                 order_date timestamp default NULL,
                 done int DEFAULT 0
            );
            """
        )

        system_print("Orders table created successfully")


def create_table_buying_transactions() -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS buying_transactions
            (
                user_id int UNIQUE,
                honey_id int NOT NULL,
                honey_amount int NOT NULL
            );
            """
        )

        system_print("Buying_transactions table created successfully")


def to_create_all_tables() -> None:
    create_table_users_info()
    create_table_users_balance()
    create_table_honey_info()
    create_table_honey_price()
    create_table_orders()
    create_table_buying_transactions()
