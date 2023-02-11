from db.io.prints import system_print, error_print


def create_table_user_info(connection):
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


def create_table_user_balance(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS users_balance (
                 id int UNIQUE,
                 balance int NOT NULL
            );
            """
        )

        system_print("Users_balance table created successfully")


def create_table_honey_info(connection):
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


def create_table_honey_price(connection):
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


def create_table_orders(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS honey_orders (
                 order_id serial PRIMARY KEY,
                 name varchar(50) NOT NULL,
                 username varchar(50) NOT NULL,
                 honey_id int NOT NULL,
                 honey_name varchar(50) NOT NULL,
                 amount int NOT NULL,
                 total int NOT NULL,
                 place varchar(50) NOT NULL,
                 comment varchar(50) NOT NULL,
                 order_date timestamp default NULL
            );
            """
        )

        system_print("Honey_orders table created successfully")


def to_create_all_tables(connection):
    create_table_user_info(connection)
    create_table_user_balance(connection)
    create_table_honey_info(connection)
    create_table_honey_price(connection)
    create_table_orders(connection)
