import psycopg2
from db.config import host, user, password, db_name, port
from db.io.prints import system_print


def connect_to_db():
    connection = None

    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            system_print(f"Success!\nServer version: {cursor.fetchone()}")

    except Exception as ex:
        system_print(f"Error while working with PostgreSQL {ex}")
    # finally:
    #     if connection:
    #         connection.close()
    #         system_print("PostgreSQL connection closed")

    return connection


def close_db(connection):
    if connection:
        connection.close()
        system_print("PostgreSQL connection closed")
