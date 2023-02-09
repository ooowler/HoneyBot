from db.io.prints import system_print, error_print


# example
def create_user_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE users (
                 id serial PRIMARY KEY,
                 balance int NOT NULL
            );
            """
        )

        system_print("Table created successfully")


def create_honey_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE honey (
                 id serial PRIMARY KEY,
                 price int NOT NULL,
                 amount int NOT NULL
            );
            """
        )

        system_print("Table created successfully")


def insert_honey(connection, honey_id, price, amount):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO
                honey(id, price, amount)
                VALUES({honey_id}, {price},{amount});
            """
        )

        system_print("Data inserted successfully")


def check_user_exist(connection, user_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select *
                from users 
                where {user_id} = users.id;
            """
        )

        result = cursor.fetchall()

        if len(result) != 0:
            error_print(f"Пользователь с id: {user_id} уже есть в базе данных")
            return True

        return False


def insert_to_user_table(connection, user_id, balance):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO
                users(id, balance)
                VALUES({user_id}, {balance});
            """
        )

        system_print("Data inserted successfully")


def deposit(connection, user_id, value) -> bool:
    user_balance = get_user_balance(connection, user_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE users SET 
                balance = '{user_balance + value}' 
                WHERE id = '{user_id}';
                """
            )

            system_print("Data inserted successfully")
            return True
    except Exception as ex:
        error_print(f"NO DEPOSIT!\n{ex}")
        return False


def buy_honey(connection, user_id, honey_id, amount_to_buy):
    error = ""
    user_balance = get_user_balance(connection, user_id)
    honey_amount = get_honey_amount(connection, honey_id)
    honey_price = get_honey_price(connection, honey_id)

    if amount_to_buy > honey_amount:
        error = f"Жаль, но такого количества меда у нас нет :("
        return error

    if user_balance < amount_to_buy * honey_price:
        error = f"Не хватает средств, пополни кошелек"
        return error

    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE users SET 
            balance = '{user_balance - amount_to_buy * honey_price}' 
            WHERE id = '{user_id}';
            """
        )

        cursor.execute(
            f"""UPDATE honey SET 
            amount = '{honey_amount - amount_to_buy}' 
            WHERE id = '{honey_id}';
            """
        )

        return True


def get_user_balance(connection, user_id) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select balance
                from users 
                where {user_id} = users.id;
            """
        )

        result = cursor.fetchall()

        if len(result) != 1:
            error_print("invalid user balance fetch")
            return -1

        system_print("Balance got successfully")
        return result[0][0]


def get_honey_amount(connection, honey_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select amount
                from honey 
                where {honey_id} = honey.id;
            """
        )

        result = cursor.fetchall()

        if len(result) != 1:
            error_print(f"no honey with {honey_id} id")
            return -1

        return result[0][0]


def get_honey_price(connection, honey_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select price
                from honey 
                where {honey_id} = honey.id;
            """
        )

        result = cursor.fetchall()

        if len(result) != 1:
            error_print(f"no honey with {honey_id} id")
            return -1

        return result[0][0]
