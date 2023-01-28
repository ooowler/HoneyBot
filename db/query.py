from db.io.prints import system_print

#example
def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE users (
                 id serial PRIMARY KEY,
                 first_name varchar(50) NOT NULL,
                 balance int NOT NULL
            );
            """
        )

        system_print("Table created successfully")
