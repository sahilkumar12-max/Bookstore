from database.db_operations import *
import sys

# Main program loop
def main():
    conn = connect()
    create_tables(conn)
    logged_in_user_id = None  # Variable to store logged-in user ID

    while True:
        print("\n=== Bookstore Management ===")
        print("1. Register")
        print("2. Login")
        print("3. Add Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. List Books")
        print("7. Search Books")
        print("8. Logout")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            logged_in_user_id = login_user(username, password)
            if logged_in_user_id:
                print("Login successful.")
        elif choice == '3':
            if logged_in_user_id:
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                genre = input("Enter book genre: ")
                price = float(input("Enter book price: "))
                quantity = int(input("Enter book quantity: "))
                add_book(title, author, genre, price, quantity)
            else:
                print("Please login first.")
        elif choice == '4':
            if logged_in_user_id:
                # Update book functionality
                book_id = int(input("Enter the ID of the book you want to update: "))
                title = input("Enter new title (leave empty to keep current): ")
                author = input("Enter new author (leave empty to keep current): ")
                genre = input("Enter new genre (leave empty to keep current): ")
                price = input("Enter new price (leave empty to keep current): ")
                quantity = input("Enter new quantity (leave empty to keep current): ")

                # Retrieve current book details
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM books WHERE id = ?''', (book_id,))
                book = cursor.fetchone()
                cursor.close()

                # Update only fields that are provided
                if title == '':
                    title = book[1]
                if author == '':
                    author = book[2]
                if genre == '':
                    genre = book[3]
                if price == '':
                    price = book[4]
                else:
                    price = float(price)
                if quantity == '':
                    quantity = book[5]
                else:
                    quantity = int(quantity)

                update_book(book_id, title, author, genre, price, quantity)
            else:
                print("Please login first.")
        elif choice == '5':
            if logged_in_user_id:
                # Delete book functionality
                book_id = int(input("Enter the ID of the book you want to delete: "))
                delete_book(book_id)
            else:
                print("Please login first.")
        elif choice == '6':
            list_books()
        elif choice == '7':
            keyword = input("Enter search keyword: ")
            search_books(keyword)
        elif choice == '8':
            logged_in_user_id = None  # Logout by resetting logged-in user ID
            print("Logged out successfully.")
        elif choice == '9':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

    # Close connection to SQLite database
    try:
        conn.close()
        print("Database connection closed.")
    except sqlite3.Error as e:
        print(f"Error closing database connection: {e}")

if __name__ == "__main__":
    main()
