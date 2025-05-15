import mysql.connector

# Database connection config
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"  # Replace with your actual password
DB_NAME = "ALX_prodev"

def stream_users():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    for row in cursor:
        yield row  # yields a dictionary row-by-row

    cursor.close()
    connection.close()
