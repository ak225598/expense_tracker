import sqlite3
import bcrypt
import datetime

# Connect to the SQLite database
conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date DATE,
        category TEXT,
        description TEXT,
        amount REAL
    )
''')

# Commit changes and close the connection
conn.commit()

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

def login_user(username, password):
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1]):
        return user_data[0]  # Return the user's ID if login is successful
    return None

def add_expense(user_id, date, category, description, amount):
    cursor.execute('INSERT INTO expenses (user_id, date, category, description, amount) VALUES (?, ?, ?, ?, ?)',
                   (user_id, date, category, description, amount))
    conn.commit()

def get_user_expenses(user_id):
    cursor.execute('SELECT id, date, category, description, amount FROM expenses WHERE user_id = ?', (user_id,))
    return cursor.fetchall()

while True:
    print("\nExpense Tracker Menu:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")
        register_user(username, password)
        print("Registration successful. Please log in.")

    elif choice == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_id = login_user(username, password)
        if user_id:
            print(f"Login successful, user ID: {user_id}")
            while True:
                print("\nExpense Tracker Menu:")
                print("1. Add Expense")
                print("2. View Expenses")
                print("3. Logout")
                inner_choice = input("Enter your choice: ")

                if inner_choice == '1':
                    date = input("Enter date (YYYY-MM-DD): ")
                    category = input("Enter category: ")
                    description = input("Enter description: ")
                    amount = float(input("Enter amount: "))
                    add_expense(user_id, date, category, description, amount)
                    print("Expense added successfully.")

                elif inner_choice == '2':
                    expenses = get_user_expenses(user_id)
                    if expenses:
                        print("\nYour Expenses:")
                        for expense in expenses:
                            print(f"ID: {expense[0]}, Date: {expense[1]}, Category: {expense[2]}, "
                                  f"Description: {expense[3]}, Amount: Rs{expense[4]}")
                    else:
                        print("No expenses found.")

                elif inner_choice == '3':
                    break

    elif choice == '3':
        break

# Close the database connection
conn.close()
