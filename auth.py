from dbm import sqlite3
from database import get_db_connection

def signup_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose another."
    finally:
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "username": user[1]}
    else:
        return None