# database/db_operations.py

import sqlite3
from bcrypt import hashpw, gensalt
from .db_config import connect

# Create tables if not exists
def create_tables(conn):
    try:
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username VARCHAR(50) UNIQUE NOT NULL,
                           password VARCHAR(100) NOT NULL
                         )''')

        # Create books table
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title VARCHAR(100) NOT NULL,
                           author VARCHAR(100) NOT NULL,
                           genre VARCHAR(50) NOT NULL,
                           price DECIMAL(10, 2) NOT NULL,
                           quantity INT NOT NULL DEFAULT 0
                         )''')

        # Create orders table
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INT NOT NULL,
                           book_id INT NOT NULL,
                           quantity INT NOT NULL,
                           order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (user_id) REFERENCES users(id),
                           FOREIGN KEY (book_id) REFERENCES books(id)
                         )''')

        conn.commit()
        cursor.close()
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

# User Management Functions

def register_user(username, password):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Hash password
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

        # Insert user into database
        cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, hashed_password))
        conn.commit()

        print("User registered successfully.")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error registering user: {e}")

def login_user(username, password):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Retrieve user from database
        cursor.execute('''SELECT id, username, password FROM users WHERE username = ?''', (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[2].encode('utf-8')
            if hashpw(password.encode('utf-8'), stored_password) == stored_password:
                print("Login successful.")
                return user[0]  # Return user ID
            else:
                print("Invalid password.")
        else:
            print("User not found.")

        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error logging in: {e}")
    return None

# Book Management Functions

def add_book(title, author, genre, price, quantity):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Insert book into database
        cursor.execute('''INSERT INTO books (title, author, genre, price, quantity)
                          VALUES (?, ?, ?, ?, ?)''', (title, author, genre, price, quantity))
        conn.commit()

        print("Book added successfully.")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error adding book: {e}")

def update_book(book_id, title, author, genre, price, quantity):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Update book information
        cursor.execute('''UPDATE books 
                          SET title = ?, author = ?, genre = ?, price = ?, quantity = ? 
                          WHERE id = ?''', (title, author, genre, price, quantity, book_id))
        conn.commit()

        print("Book updated successfully.")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error updating book: {e}")

def delete_book(book_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Delete book
        cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
        conn.commit()

        print("Book deleted successfully.")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error deleting book: {e}")

def list_books():
    try:
        conn = connect()
        cursor = conn.cursor()

        # Retrieve books from database
        cursor.execute('''SELECT * FROM books''')
        books = cursor.fetchall()

        if books:
            print("ID | Title | Author | Genre | Price | Quantity")
            print("-" * 60)
            for book in books:
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]}")
        else:
            print("No books found.")

        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error listing books: {e}")

def search_books(keyword):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Search books by title or author
        cursor.execute('''SELECT * FROM books WHERE title LIKE ? OR author LIKE ?''', (f"%{keyword}%", f"%{keyword}%"))
        books = cursor.fetchall()

        if books:
            print("ID | Title | Author | Genre | Price | Quantity")
            print("-" * 60)
            for book in books:
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]}")
        else:
            print("No books found.")

        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error searching books: {e}")
