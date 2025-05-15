# 📘 Python Generators: Streaming Data from SQL

This project demonstrates how to use **Python generators** to efficiently stream, batch, and process data from a **MySQL database**. It showcases memory-efficient techniques using yield for large datasets in a backend environment.

---

## 🗄️ Database Setup

Before running the scripts, ensure you have:
- A MySQL server running
- A database named ALX_prodev
- A table user_data with the following fields:
  - user_id (UUID, Primary Key, Indexed)
  - name (VARCHAR, NOT NULL)
  - email (VARCHAR, NOT NULL)
  - age (DECIMAL, NOT NULL)

### 🛠️ Seed Script (seed.py)

This script sets up the database and loads sample data from user_data.csv.

**Functions:**
python
### def connect_db(): 
    # Connects to MySQL server

### def create_database(connection): 
    # Creates ALX_prodev if it does not exist

### def connect_to_prodev(): 
    # Connects to ALX_prodev database

### def create_table(connection): 
    # Creates user_data table with the required schema

### def insert_data(connection, data): 
    # Inserts user data from CSV into the table
🧩 Generator-Based Scripts
0-stream_users.py
Streams users one-by-one using a Python generator.

Function:

python

### def stream_users()
Yields each row as a dictionary.

Memory-efficient: fetches one row at a time.

1-batch_processing.py
Fetches users in batches and filters those over the age of 25.

Functions:

### def stream_users_in_batches(batch_size): 
    # Yields a batch of rows as a list of dictionaries

### def batch_processing(batch_size): 
    # Filters and yields users over 25 from each batch
2-lazy_paginate.py
Implements lazy pagination — loads the next page of users only when needed.

Functions:

### def paginate_users(page_size, offset): 
    # Returns rows using LIMIT + OFFSET

### def lazy_pagination(page_size): 
    # Generator that yields one page at a time lazily
3-average_age.py
Computes the average age of users without SQL AVG() and without loading all data into memory.

Functions:

### def stream_user_ages(): 
    # Yields ages one by one from the database

### def compute_average_age(): 
    # Calculates average using a generator and minimal memory
🚀 Usage
Ensure your MySQL credentials in seed.py are correct.

Run the seed script:

python seed.py
Test main scripts:

python 1-main.py
python 2-main.py
python 3-main.py
To see only part of the output (e.g., first 5 lines):
