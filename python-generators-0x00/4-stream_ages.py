import seed

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    for (age,) in cursor:
        yield float(age)  # Cast to float for precise average

    cursor.close()
    connection.close()

def compute_average_age():
    """
    Computes average age using a generator, without loading all data into memory.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # First and only loop
        total += age
        count += 1

    average = total / count if count else 0
    print(f"Average age of users: {average:.2f}")
