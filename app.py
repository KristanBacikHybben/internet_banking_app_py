import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from datetime import datetime
import sqlite3
from payment_data import *

balance_value = 5000

def new_window(tab_name):
    frame = ttk.Frame(root)
    notebook.add(frame, text=tab_name)
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
            global balance_value
            try:
                amount = float(payment_amount_input.get())
                if amount <= balance_value:
                    payment_data = (
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

                    balance_value -= amount
                    balance_display.config(text=f"Your Balance: {balance_value}€")
                    messagebox.showinfo("Success", "Payment signed and transferred!")
                else:
                    messagebox.showinfo("Not enough balance")
                    return
            except ValueError:
                messagebox.showinfo("Invalid Amount")
        sign_transfer_button = ttk.Button(frame, text="Sign and transfer", command=sign_and_transfer)
        sign_transfer_button.pack()
    elif tab_name == "Settings":
        details_label = ttk.Label(frame, text="Product details")
        details_label.pack()
        current_balance_detail = ttk.Label(frame, text=f"Current Balance: {balance_value}")
        current_balance_detail.pack()
        your_iban_value = "SK73 0100 0000 0015 6153 4661"
        your_iban = ttk.Label(frame, text=f"IBAN: {your_iban_value}")
        your_iban.pack()
        account_number_value = "6493683369/0200"
        account_number = ttk.Label(frame, text=f"Account Number: {account_number_value}")
        account_number.pack()
        bic_swift_value = "ZITASKBX"
        bic_swift = ttk.Label(frame, text=f"BIC/SWIFT: {bic_swift_value}")
        bic_swift.pack()
        monthly_fee_value = 3
        monthly_fee = ttk.Label(frame, text=f"Monthly fee: {monthly_fee_value}")
        monthly_fee.pack()
    elif tab_name == "Account Statements":
        statement_label = ttk.Label(frame, text="Statements")
        statement_label.pack()
        add_statement_button = ttk.Button(frame, text="New statement rule")
        add_statement_button.pack()
    elif tab_name == "History":
        tree = ttk.Treeview(frame)

        tree["column"] = ("id",
                        "name",
                        "iban",
                        "amount",
                        "variable_symbol",
                        "constant_symbol",
                        "specific_symbol",
                        "message_for_recipient",
                        "sender_reference",
                        "timestamp")
        for col in tree["column"]:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100)

        db_cursor.execute("SELECT * FROM payments")
        rows = db_cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)
        
        tree.pack(expand=True, fill="both")

root = tk.Tk()

window_width = 1920
window_height = 1080

root.geometry(f"{window_width}x{window_height}")

root.title("BanKing")

notebook = ttk.Notebook(root)

balance_display = ttk.Label(root, text=f" Your Balance: {balance_value}€")
balance_display.pack()


history_button = ttk.Button(root, text="History", command=lambda: new_window("History"))
history_button.pack(side="top")

new_payment_button = ttk.Button(root, text="New Payment", command=lambda: new_window("New Payment"))
new_payment_button.pack(side="top")


account_statements_button = ttk.Button(root, text="Account Statements", command=lambda: new_window("Account Statements"))
account_statements_button.pack(side="top")

standing_orders_button = ttk.Button(root, text="Standing Orders", command=lambda: new_window("Standing Orders"))
standing_orders_button.pack(side="top")


settings_button = ttk.Button(root, text="Settings", command=lambda: new_window("Settings"))
settings_button.pack(side="top")

notebook.pack(expand=True, fill="both")

root.mainloop()