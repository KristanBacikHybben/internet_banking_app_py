import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from datetime import datetime
import sqlite3
import random
import string
from payment_data import *

current_user = None

class SettingsTab:
    def __init__(self, frame, user_details):
        self.frame = frame
        self.user_details = user_details
        

    def create(self):
        db_cursor.execute("SELECT balance FROM users WHERE id = ?", (self.user_details["id"],))
        latest_balance = db_cursor.fetchone()
        self.user_details["balance"] = latest_balance[0] if latest_balance else self.user_details["balance"]

        self.current_balance_detail = ttk.Label(self.frame, text=f"Current Balance: {self.user_details['balance']}€")
        self.current_balance_detail.pack()

        your_iban = ttk.Label(self.frame, text=f"IBAN: {self.user_details['iban']}")
        your_iban.pack()

        account_number_label = ttk.Label(self.frame, text=f"Account Number: {self.user_details['account_number']}")
        account_number_label.pack()

        bic_swift_label = ttk.Label(self.frame, text=f"BIC/SWIFT: {self.user_details['bic_swift']}")
        bic_swift_label.pack()

        monthly_fee_label = ttk.Label(self.frame, text=f"Monthly Fee: {self.user_details['monthly_fee']}")
        monthly_fee_label.pack()

        return self

window_width = 1080
window_height = 720

root = tk.Tk()

def generate_unique_iban():
    return "SK" + "".join(random.choices(string.digits, k=20))

def generate_unique_account_number():
    return "".join(random.choices(string.digits, k=10)) + "/0200"

def generate_unique_bic_swift():
    return "ZITA" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

def login_screen():
    login_window = tk.Toplevel(root)
    login_window.geometry(f"{window_width}x{window_height}")
    login_window.title("Login")

    username_label = ttk.Label(login_window, text="Username")
    username_label.pack()

    username_entry = ttk.Entry(login_window)
    username_entry.pack()

    password_label = ttk.Label(login_window, text="Password")
    password_label.pack()

    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack()

    def handle_login():
        user = login_user(username_entry.get(), password_entry.get())
        if user:
            global current_user
            current_user = user
            messagebox.showinfo("SUCCESS", "Logged in")
            login_window.destroy()

            login_menu_button.destroy()
            register_button.destroy()

            history_button.pack()
            new_payment_button.pack()
            account_statements_button.pack()
            settings_button.pack()

        else:
            messagebox.showerror("ERROR", "Wrong username or password")

    ttk.Button(login_window, text="Login", command=handle_login).pack()

def register_screen():
    register_window = tk.Toplevel(root)
    register_window.geometry(f"{window_width}x{window_height}")
    register_window.title("Register")

    username_label = ttk.Label(register_window, text="Username")
    username_label.pack()

    username_entry = ttk.Entry(register_window)
    username_entry.pack()

    password_label = ttk.Label(register_window, text="Password")
    password_label.pack()

    password_entry = ttk.Entry(register_window)
    password_entry.pack()

    def handle_register():
        registered = register_user(username_entry.get(), password_entry.get())
        if registered:
            messagebox.showinfo("SUCCESS", "Registration successful")
            register_window.destroy()
        else:
            messagebox.showerror("ERROR", "Username is already taken")

    ttk.Button(register_window, text="Register", command=handle_register).pack()

login_menu_button = ttk.Button(root, text="Login", command=login_screen)
login_menu_button.pack(side="top")

register_button = ttk.Button(root, text="Register", command=register_screen)
register_button.pack(side="top")

def register_user(username, password):
    iban = generate_unique_iban()
    account_number = generate_unique_account_number()
    bic_swift = generate_unique_bic_swift()
    balance = 5000
    monthly_fee = 3
    try:
        db_cursor.execute("INSERT INTO users (username, password, balance, iban, account_number, bic_swift, monthly_fee) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (username, password, balance, iban, account_number, bic_swift, monthly_fee))
        db_conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    
def login_user(username, password):
    db_cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = db_cursor.fetchone()
    return user

def new_window(tab_name):
    frame = ttk.Frame(root)
    notebook.add(frame, text=tab_name)

    

    db_cursor.execute("SELECT id, balance, iban, account_number, bic_swift FROM users WHERE id = ?", (current_user[0],))
    user_details = db_cursor.fetchone()
    user_details = {
        'id': user_details[0],
        'balance': user_details[1],
        'iban': user_details[2],
        'account_number': user_details[3],
        'bic_swift': user_details[4],
        'monthly_fee': 3
    }
    

    history_table = ttk.Treeview(frame)
    history_table["column"] = ("id", "name", "iban", "amount", "variable_symbol", "constant_symbol", "specific_symbol", "message_for_recipient", "sender_reference", "timestamp")

    def filling_the_history_table(history_table, db_cursor):
        for col in history_table["column"]:
            history_table.heading(col, text=col.capitalize())
            history_table.column(col, width=100)

        db_cursor.execute("SELECT * FROM payments WHERE user_id = ?", (current_user[0],))
        rows = db_cursor.fetchall()

        for row in rows:
            history_table.insert("", "end", values=row)

    if tab_name == "New Payment":
        payment_name = ttk.Label(frame, text="Name")
        payment_name.pack()

        payment_name_input = ttk.Entry(frame)
        payment_name_input.pack()

        payment_iban = ttk.Label(frame, text="IBAN/Account Number")
        payment_iban.pack()

        payment_iban_input = ttk.Entry(frame)
        payment_iban_input.pack()

        payment_amount = ttk.Label(frame, text="Amount")
        payment_amount.pack()

        payment_amount_input = ttk.Entry(frame)
        payment_amount_input.pack()

        variable_symbol = ttk.Label(frame, text="Variable symbol")
        variable_symbol.pack()
        variable_symbol_input = ttk.Entry(frame)
        variable_symbol_input.pack()

        constant_symbol = ttk.Label(frame, text="Constant symbol")
        constant_symbol.pack()
        constant_symbol_input = ttk.Entry(frame)
        constant_symbol_input.pack()

        specific_symbol = ttk.Label(frame, text="Specific symbol")
        specific_symbol.pack()
        specific_symbol_input = ttk.Entry(frame)
        specific_symbol_input.pack()

        message_for_recepient = ttk.Label(frame, text="Message for the recepient")
        message_for_recepient.pack()
        message_for_recipient_input = ttk.Entry(frame)
        message_for_recipient_input.pack()

        sender_refference = ttk.Label(frame, text="Sender refference")
        sender_refference.pack()
        sender_reference_input = ttk.Entry(frame)
        sender_reference_input.pack()

        def sign_and_transfer():
            nonlocal settings_tab
            try:
                amount = float(payment_amount_input.get())
                if amount > user_details['balance']:
                    messagebox.showerror("", "Not enough balance")
                    return
                else:
                    new_balance = user_details["balance"] - amount
                    db_cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, current_user[0]))
                    db_conn.commit()

                    user_details["balance"] = new_balance

                    #settings_tab.current_balance_detail.config(text=f"Current Balance: {user_details['balance']}€")

                    payment_data = (
                        current_user[0],
                        payment_name_input.get(),
                        payment_iban_input.get(),
                        amount,
                        variable_symbol_input.get(),
                        constant_symbol_input.get(),
                        specific_symbol_input.get(),
                        message_for_recipient_input.get(),
                        sender_reference_input.get(),
                        datetime.now()
                    )
                        
                    insert_payment(payment_data)

                    user_details['balance'] -= amount
                    #settings_tab.current_balance_detail.config(text=f"Current Balance: {user_details['balance']}€")

                    messagebox.showinfo("", "Payment signed and funds have been successfuly transferred")
                    
            except ValueError:
                messagebox.showinfo("Invalid Amount")
        sign_transfer_button = ttk.Button(frame, text="Sign and transfer", command=lambda: sign_and_transfer())
        sign_transfer_button.pack()
    elif tab_name == "Settings":           
        settings_tab = SettingsTab(frame, user_details)
        settings_tab.create()
    elif tab_name == "Account Statements":
        def generate_statement():
            generated_statement_frame = ttk.Frame(notebook)
            notebook.add(generated_statement_frame, text="Statement")
            detail_table = ttk.Treeview(generated_statement_frame, columns=("Property", "Value"))
            detail_table.heading("Property", text="Property")
            detail_table.heading("Value", text="Value")

            detail_table.insert("", "end", values=("Balance", user_details['balance']))
            detail_table.insert("", "end", values=("IBAN", user_details['iban']))
            detail_table.insert("", "end", values=("Account Number", user_details['account_number']))
            detail_table.insert("", "end", values=("BIC/SWIFT", user_details['bic_swift']))
            detail_table.insert("", "end", values=("Monthly Fee", user_details['monthly_fee']))
            detail_table.pack(expand=True, anchor="n", fill="x")

            history_table = ttk.Treeview(generated_statement_frame, columns=("id", "name", "iban", "amount", "variable_symbol", "constant_symbol", "specific_symbol", "message_for_recipient", "sender_reference", "timestamp"))
            filling_the_history_table(history_table, db_cursor)
            history_table.pack(expand=True, fill="both")

        latest_statement = ttk.Button(frame, text="Latest statement", command=generate_statement)
        latest_statement.pack()
    elif tab_name == "History":
        filling_the_history_table(history_table, db_cursor)
        history_table.pack(expand=True, fill="both")

root.geometry(f"{window_width}x{window_height}")

root.title("BanKing")

notebook = ttk.Notebook(root)


history_button = ttk.Button(root, text="History", command=lambda: new_window("History"))
new_payment_button = ttk.Button(root, text="New Payment", command=lambda: new_window("New Payment"))
account_statements_button = ttk.Button(root, text="Account Statements", command=lambda: new_window("Account Statements"))
settings_button = ttk.Button(root, text="Settings", command=lambda: new_window("Settings"))
notebook.pack(expand=True, fill="both")

root.mainloop()