import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from datetime import datetime
import sqlite3
from payment_data import *

class SettingsTab:
    def __init__(self,frame,balance_value,iban,account_number,bic_swift,monthly_fee):
        self.frame = frame
        self.balance_value = balance_value
        self.iban = iban
        self.account_number = account_number
        self.bic_swift = bic_swift
        self.monthly_fee = monthly_fee
    def create(self):
        current_balance_detail = ttk.Label(self.frame, text=f"Current Balance: {self.balance_value}€")
        current_balance_detail.pack()

        your_iban = ttk.Label(self.frame, text=f"IBAN: {self.iban}")
        your_iban.pack()

        account_number_label = ttk.Label(self.frame, text=f"Account Number: {self.account_number}")
        account_number_label.pack()

        bic_swift_label = ttk.Label(self.frame, text=f"BIC/SWIFT: {self.bic_swift}")
        bic_swift_label.pack()

        monthly_fee_label = ttk.Label(self.frame, text=f"Monthly Fee: {self.monthly_fee}")
        monthly_fee_label.pack()

balance_value = 5000

def new_window(tab_name):
    frame = ttk.Frame(root)
    notebook.add(frame, text=tab_name)
    settings_tab = SettingsTab(
                frame,
                balance_value=balance_value,
                iban="SK73 0100 0000 0015 6153 4661",
                account_number="6493683369/0200",
                bic_swift="ZITASKBX",
                monthly_fee=3
            )
    
    history_table = ttk.Treeview(frame)

    history_table["column"] = ("id",
                        "name",
                        "iban",
                        "amount",
                        "variable_symbol",
                        "constant_symbol",
                        "specific_symbol",
                        "message_for_recipient",
                        "sender_reference",
                        "timestamp")
    
    def filling_the_history_table(history_table, db_cursor):        
        for col in history_table["column"]:
            history_table.heading(col, text=col.capitalize())
            history_table.column(col, width=100)

        db_cursor.execute("SELECT * FROM payments")
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
            global balance_value
            try:
                amount = float(payment_amount_input.get())
                if amount > balance_value:
                    messagebox.showerror("", "Not enough balance")
                    return
                else:
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
                    balance_display.config(text=f"Current Balance: {balance_value}€")
                    messagebox.showinfo("", "Payment signed and funds have been successfuly transferred")
            except ValueError:
                messagebox.showinfo("Invalid Amount")
        sign_transfer_button = ttk.Button(frame, text="Sign and transfer", command=sign_and_transfer)
        sign_transfer_button.pack()
    elif tab_name == "Settings":         
            
            settings_tab.create()
    elif tab_name == "Account Statements":
        def generate_statement():
            generated_statement_frame = ttk.Frame(notebook)
            notebook.add(generated_statement_frame, text="statement")
            detail_table = ttk.Treeview(generated_statement_frame, columns=("Property","Value"))
            detail_table.heading("Property")
            detail_table.heading("Value")
            
            detail_table.insert("", "end", values=("Balance", settings_tab.balance_value))
            detail_table.insert("", "end", values=("IBAN", settings_tab.iban))
            detail_table.insert("", "end", values=("Account Number", settings_tab.account_number))
            detail_table.insert("", "end", values=("BIC/SWIFT", settings_tab.bic_swift))
            detail_table.insert("", "end", values=("Monthly Fee", settings_tab.monthly_fee))
            detail_table.pack(expand=True, anchor="n", fill="x")
            history_table = ttk.Treeview(generated_statement_frame, columns=("id",
                         "name",
                        "iban",
                        "amount",
                        "variable_symbol",
                        "constant_symbol",
                        "specific_symbol",
                        "message_for_recipient",
                        "sender_reference",
                        "timestamp"))
            
            filling_the_history_table(history_table, db_cursor)
            history_table.pack(expand=True, fill="both")
            
        latest_statement = ttk.Button(frame, text="Statement", command=generate_statement)
        latest_statement.pack()
    elif tab_name == "History":
        filling_the_history_table(history_table, db_cursor)
        history_table.pack(expand=True, fill="both")

root = tk.Tk()

window_width = 1920
window_height = 1080

root.geometry(f"{window_width}x{window_height}")

root.title("BanKing")

notebook = ttk.Notebook(root)

balance_display = ttk.Label(root, text=f"Current Balance: {balance_value}€")
balance_display.pack()

history_button = ttk.Button(root, text="History", command=lambda: new_window("History"))
history_button.pack(side="top")

new_payment_button = ttk.Button(root, text="New Payment", command=lambda: new_window("New Payment"))
new_payment_button.pack(side="top")

account_statements_button = ttk.Button(root, text="Account Statements", command=lambda: new_window("Account Statements"))
account_statements_button.pack(side="top")

settings_button = ttk.Button(root, text="Settings", command=lambda: new_window("Settings"))
settings_button.pack(side="top")

notebook.pack(expand=True, fill="both")

root.mainloop()