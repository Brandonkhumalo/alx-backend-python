import mysql.connector

# Database connection configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"  # Replace with your actual password
DB_NAME = "ALX_prodev"

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of user records from the user_data table.
    Each batch is a list of dictionaries (one per row).
    """
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    
    # Using a single loop to fetch rows in batches
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes batches of user records and yields only those with age > 25.
    Uses the stream_users_in_batches generator to obtain data.
    """
    # First loop: iterate over each batch from the generator
    for batch in stream_users_in_batches(batch_size):
        # Second loop: iterate through users within the current batch
        for user in batch:
            # Filter condition: only users over the age of 25
            if float(user['age']) > 25:
                yield user

