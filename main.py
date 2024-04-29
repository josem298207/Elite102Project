import mysql.connector
from tkinter import *

# Connect to MySQL database
db = mysql.connector.connect(
    user="root",
    password="DeltaCharlie27!",
    database="bank"
)
cursor = db.cursor()

# Create tables if they don't exist
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), balance DECIMAL(10, 2))")
cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id INT AUTO_INCREMENT PRIMARY KEY, account_id INT, type ENUM('deposit', 'withdrawal'), amount DECIMAL(10, 2), FOREIGN KEY (account_id) REFERENCES accounts(id))")

# Create Tkinter GUI
root = Tk()
root.title("The bank of Jose")

# Creates an account with a name and balance
def create_account():
    name = name_entry.get()
    balance = float(balance_entry.get())
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
    db.commit()
    update_accounts_list()

#tried to figure out account deletion but could not attempt it
def update_accounts_list():
    cursor.execute("SELECT id, name, balance FROM accounts")
    accounts = cursor.fetchall()
    accounts_listbox.delete(0, END)
    for account in accounts:
        accounts_listbox.insert(END, f"ID: {account[0]}, Name: {account[1]}, Balance: {account[2]}")

# deposits money into a certain bank account
def deposit():
    account_id = int(account_id_entry.get())
    amount = float(amount_entry.get())
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, 'deposit', %s)", (account_id, amount))
    db.commit()
    update_accounts_list()

# withdraws money from a certain bank account
def withdraw():
    account_id = int(account_id_entry.get())
    amount = float(amount_entry.get())
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, 'withdrawal', %s)", (account_id, amount))
        db.commit()
        update_accounts_list()
    else:
        error_label.config(text="Insufficient balance")

# creates the name label
name_label = Label(root, text="Name:")
name_label.pack()
name_entry = Entry(root)
name_entry.pack()

# creates the initial balance label when starting a new account
balance_label = Label(root, text="Initial Balance:")
balance_label.pack()
balance_entry = Entry(root)
balance_entry.pack()


#creates the create account button
create_account_button = Button(root, text="Create Account", command=create_account)
create_account_button.pack()

accounts_listbox = Listbox(root, height=10, width=50)
accounts_listbox.pack()

#creates the account id label
account_id_label = Label(root, text="Account ID:")
account_id_label.pack()
account_id_entry = Entry(root)
account_id_entry.pack()

# creates the amount label
amount_label = Label(root, text="Amount:")
amount_label.pack()
amount_entry = Entry(root)
amount_entry.pack()

#creates the withdraw button
withdraw_button = Button(root, text="Withdraw", command=withdraw)
withdraw_button.pack()

#creates the deposit button
deposit_button = Button(root, text="Deposit", command=deposit)
deposit_button.pack()

error_label = Label(root, text="", fg="red")
error_label.pack()

update_accounts_list()

root.mainloop()