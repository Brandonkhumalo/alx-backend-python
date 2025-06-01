#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime  # ✅ Required import

# Decorator to log SQL queries with timestamp
def log_queries(func):
    """Decorator that logs the SQL query with a timestamp before executing the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else 'UNKNOWN QUERY')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetches all users from the database using the provided SQL query."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
