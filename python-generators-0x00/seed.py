import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"  # Replace with your actual password

# Connect to MySQL server (no specific database)
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Create the ALX_prodev database
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ensured.")
    finally:
        cursor.close()

# Connect to the ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database="ALX_prodev"
    )

# Create the user_data table if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            )
        """)
        print("Table user_data ensured.")
    finally:
        cursor.close()

# Insert data into user_data table if it doesn't already exist
def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            name, email, age = row
            # Check for duplicates
            cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
            if cursor.fetchone():
                continue
            user_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, name, email, age)
            )
        connection.commit()
        print("Data inserted successfully.")
    finally:
        cursor.close()

# Load data from CSV
def load_csv_data(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [row for row in reader]

if __name__ == "__main__":
    try:
        conn = connect_db()
        create_database(conn)
        conn.close()

        conn_prodev = connect_to_prodev()
        create_table(conn_prodev)

        data = load_csv_data("user_data.csv")
        insert_data(conn_prodev, data)
        conn_prodev.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied. Check your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
