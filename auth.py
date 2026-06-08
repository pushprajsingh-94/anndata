import sqlite3
import hashlib
import os

DB_PATH = "data/farmers.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS farmers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT UNIQUE NOT NULL,
                  district TEXT NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_farmer(name, phone, district, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO farmers (name, phone, district, password) VALUES (?, ?, ?, ?)",
                  (name, phone, district, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_farmer(phone, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM farmers WHERE phone=? AND password=?",
              (phone, hash_password(password)))
    farmer = c.fetchone()
    conn.close()
    if farmer:
        return {"id": farmer[0], "name": farmer[1], "phone": farmer[2], "district": farmer[3]}
    return None

init_db()