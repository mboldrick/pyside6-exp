# create_database.py
# From the book "Beginning Pyqt - A Hands-on Approach to GUI Programming", 2nd Edition
# Chapter 14

import sys
import random
from PySide6.QtSql import QSqlDatabase, QSqlQuery


class CreateEmployeeData:
    """Create a sample database for the project."""
    # Create a connection to the database. If the db file does not exist,
    # it will be created.
    # Use the SQLite version 3 driver.
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("data/accounts.db")

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1)

    # Create a query object.
    query = QSqlQuery()

    # Erase the tables if they already exist.
    query.exec("DROP TABLE IF EXISTS accounts")
    query.exec("DROP TABLE IF EXISTS countries")

    # Create the tables.
    query.exec("""CREATE TABLE accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        employee_id INTEGER NOT NULL,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        email VARCHAR(50) NOT NULL,
        department VARCHAR(30) NOT NULL,
        country_id VARCHAR(20) REFERENCES countries(id)
        )""")

    # Positional binding to insert records into the database.
    query.prepare("""INSERT INTO accounts (
        employee_id, first_name, last_name, email, department, country_id
        ) VALUES (?, ?, ?, ?, ?, ?)""")
