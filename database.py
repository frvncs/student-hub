import sqlite3
from pathlib import Path

DB_FILE = "student_hub.db"

def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Notes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        type TEXT,
        content TEXT,
        pinned BOOLEAN DEFAULT 0,
        date TEXT,
        archived BOOLEAN DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Tasks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        Task TEXT NOT NULL,
        Deadline TEXT,
        SubmissionTime TEXT,
        Priority TEXT,
        Progress TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Budgets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        budget REAL DEFAULT 0,
        budget_type TEXT DEFAULT 'Monthly',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Expenses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        Category TEXT,
        Amount REAL,
        Date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()