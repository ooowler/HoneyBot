from db.io.prints import system_print, error_print



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


def insert_honey(connection, honey_id, price, amount):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO
                honey(id, price, amount)
                VALUES({honey_id}, {price},{amount});
            """
        )

        system_print("Data inserted successfully")


def buy_honey(connection, user_id, user_balance, honey_id, amount_to_buy):
    error = ""
    # user_balance = get_user_balance(connection, user_id)
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
