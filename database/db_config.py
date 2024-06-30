# database/db_config.py

import sqlite3

DB_NAME = 'bookstore.db'  # SQLite database file

def connect():
    conn = sqlite3.connect(DB_NAME)
    print('Connected to SQLite database')
    return conn
