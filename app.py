import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


root = tk.Tk()

window_width = 1920
window_height = 1080

root.geometry(f"{window_width}x{window_height}")

root.title("BanKing")

notebook = ttk.Notebook(root)

history_frame = ttk.Frame(notebook)
notebook.add(history_frame, text="History")

new_payment = ttk.Frame(notebook)
notebook.add(new_payment, text="New payment")


account_statements = ttk.Frame(notebook)
notebook.add(account_statements, text="Account statements")

standing_orders = ttk.Frame(notebook)
notebook.add(standing_orders, text="Standing orders")


settings = ttk.Frame(notebook)
notebook.add(settings, text="Settings")

notebook.pack()

root.mainloop()