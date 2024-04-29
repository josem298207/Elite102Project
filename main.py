import mysql.connector
from tkinter import *

# Establish connection to the MySQL database using the mysql.connector library
db = mysql.connector.connect(
    user="root",  # MySQL database user
    password="DeltaCharlie27!",  # MySQL database password
    database="bank"  # Database name
)
cursor = db.cursor()

# Execute SQL commands to create necessary tables if they don't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(255), 
        balance DECIMAL(10, 2)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        account_id INT, 
        type ENUM('deposit', 'withdrawal'), 
        amount DECIMAL(10, 2), 
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
""")

# Initialize Tkinter window for the GUI
root = Tk()
root.title("The bank of Jose")  # Set the window title

# Function to create a new bank account
def create_account():
    name = name_entry.get()  # Get the name from the entry box
    balance = float(balance_entry.get())  # Get the initial balance and convert to float
    # Insert the new account data into the accounts table
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
    db.commit()  # Commit changes to the database
    update_accounts_list()  # Update the list of accounts in the GUI

# Tried to figure out account deletion woould have been here. Could not figure it out on time.

# Function to refresh the list of accounts displayed in the GUI
def update_accounts_list():
    cursor.execute("SELECT id, name, balance FROM accounts")
    accounts = cursor.fetchall()  # Fetch all rows from the accounts table
    accounts_listbox.delete(0, END)  # Clear the current listbox items
    for account in accounts:
        accounts_listbox.insert(END, f"ID: {account[0]}, Name: {account[1]}, Balance: {account[2]}")

# Function to deposit money into an account
def deposit():
    account_id = int(account_id_entry.get())  # Get the account ID from the entry box
    amount = float(amount_entry.get())  # Get the deposit amount and convert to float
    # Update the account balance and insert a new transaction record
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, 'deposit', %s)", (account_id, amount))
    db.commit()  # Commit changes to the database
    update_accounts_list()  # Refresh the GUI list of accounts

# Function to withdraw money from an account
def withdraw():
    account_id = int(account_id_entry.get())  # Get the account ID from the entry box
    amount = float(amount_entry.get())  # Get the withdrawal amount and convert to float
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cursor.fetchone()[0]  # Retrieve the current balance
    if balance >= amount:  # Check if the balance is sufficient for withdrawal
        # Update the account balance and log the transaction
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, 'withdrawal', %s)", (account_id, amount))
        db.commit()  # Commit changes to the database
        update_accounts_list()  # Refresh the GUI list of accounts
    else:
        error_label.config(text="Insufficient balance")  # Display error if balance is insufficient

# GUI setup for creating and interacting with accounts

# Creates the name label
name_label = Label(root, text="Name:")
name_label.pack()
name_entry = Entry(root)
name_entry.pack()

# Creates the initial balance label when starting a new account
balance_label = Label(root, text="Initial Balance:")
balance_label.pack()
balance_entry = Entry(root)
balance_entry.pack()

# Creates the create account button
create_account_button = Button(root, text="Create Account", command=create_account)
create_account_button.pack()

accounts_listbox = Listbox(root, height=10, width=50)
accounts_listbox.pack()

# Creates the account id label
account_id_label = Label(root, text="Account ID:")
account_id_label.pack()
account_id_entry = Entry(root)
account_id_entry.pack()

# Creates the amount label
amount_label = Label(root, text="Amount:")
amount_label.pack()
amount_entry = Entry(root)
amount_entry.pack()

# Creates the withdraw button
withdraw_button = Button(root, text="Withdraw", command=withdraw)
withdraw_button.pack()

# Creates the deposit button
deposit_button = Button(root, text="Deposit", command=deposit)
deposit_button.pack()

error_label = Label(root, text="", fg="red")
error_label.pack()

update_accounts_list()  # Initialize the account list on GUI start

root.mainloop()  # Start the GUI main loop
