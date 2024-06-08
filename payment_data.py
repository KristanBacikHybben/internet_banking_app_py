import sqlite3

db_conn = sqlite3.connect("payments.db")
db_cursor = db_conn.cursor()

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    iban TEXT,
    amount REAL,
    variable_symbol TEXT,
    constant_symbol TEXT,
    specific_symbol TEXT,
    message_for_recipient TEXT,
    sender_reference TEXT,
    timestamp DATETIME
)
""")
db_conn.commit()

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT)
""")
db_conn.commit()

def insert_payment(user_id, data):
    db_cursor.execute("""
    INSERT INTO payments (
        user_id, name, iban, amount, variable_symbol, constant_symbol, specific_symbol, 
        message_for_recipient, sender_reference, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, *data))
    db_conn.commit()