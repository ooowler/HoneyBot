from db.io.prints import system_print, error_print


# example
def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE users (
                 id serial PRIMARY KEY,
                 balance int NOT NULL
            );
            """
        )

        system_print("Table created successfully")


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
            error_print(f"пользователь с id: {user_id} уже есть в базе данных")
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
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE users SET 
            balance = '{user_balance + value}' 
            WHERE id = '{user_id}';
            """
        )

        system_print("Data inserted successfully")
        return True


def withdraw(connection, user_id, value) -> bool:
    user_balance = get_user_balance(connection, user_id)
    with connection.cursor() as cursor:
        if user_balance - value < 0:
            error_print(f"user: {user_id} don't have enough money")
            return False

        cursor.execute(
            f"""UPDATE users SET 
            balance = '{user_balance - value}' 
            WHERE id = '{user_id}';
            """
        )

        system_print("Data inserted successfully")
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
