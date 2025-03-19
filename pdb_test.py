import sqlite3
from datetime import datetime
from prettytable import PrettyTable


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
        VALUES ('Jane Doe', 'individual', NULL, '   ', '555-555-5556');
    """
    c.execute(sql)
    person_id = c.lastrowid
    print("Person ID:", person_id)
    conn.commit()
    c.close()
    print("Data inserted successfully")

def add_person(conn, name, type, company_name, email, phone):
    c = conn.cursor()
    sql = """
        INSERT INTO people (name, type, company_name, email, phone)
        VALUES (?, ?, ?, ?, ?);
    """
    c.execute(sql, (name, type, company_name, email, phone))
    person_id = c.lastrowid
    conn.commit()
    c.close()
    return person_id

def get_all_people(conn):
    c = conn.cursor()
    sql = """
        SELECT * FROM people;
    """
    c.execute(sql)
    rows = c.fetchall()
    c.close()
    return rows

conn = open_database()
create_table(conn)
# create_data(conn)
people = get_all_people(conn)
t = PrettyTable(['Id', 'Name', 'Type', 'Company', 'Email', 'Phone', 'Created At'])
for (id, name, type, company_name, email, phone, created_at) in people:
    t.add_row([id, name, type, company_name, email, phone, created_at])
print(t)
conn.close()
print("Connection closed")
