import sqlite3
from datetime import datetime


def open_database():
    db = "pydb.db"

    print("Connecting to SQLite database:", db)
    conn = sqlite3.connect(db)
    print('Connection:', conn)

    return conn

def create_table(conn):
    c = conn.cursor()
    sql = """
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT CHECK (type IN ('individual', 'company')),
            company_name TEXT,
            email TEXT,
            phone TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """

    c.execute(sql)
    conn.commit()
    print("Table created successfully")

def create_data(conn):
    c = conn.cursor()
    sql = """
        INSERT INTO people (name, type, company_name, email, phone)
        VALUES ('John Doe', 'individual', NULL, '   ', '555-5555');
    """
    c.execute(sql)
    person_id = c.lastrowid
    print("Person ID:", person_id)
    conn.commit()
    c.close()
    print("Data inserted successfully")


conn = open_database()
create_table(conn)
create_data(conn)
conn.close()
print("Connection closed")
