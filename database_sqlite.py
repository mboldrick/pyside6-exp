
import sqlite3

class Database:
    def __init__(self, db_name="billing.db"):
        """
        Initialize the database connection.
        """
        self.db_name = db_name
        self.connection = self._connect_sqlite()
        self._ensure_tables_exist()

    def _connect_sqlite(self):
        return sqlite3.connect(self.db_name)

    def _ensure_tables_exist(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS expense_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category_id INTEGER,
                description TEXT,
                date TEXT,
                FOREIGN KEY (category_id) REFERENCES expense_categories(id)
            );
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT
            );
            CREATE TABLE IF NOT EXISTS work_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                project_id INTEGER,
                hours REAL,
                date TEXT,
                FOREIGN KEY (person_id) REFERENCES people(id),
                FOREIGN KEY (project_id) REFERENCES projects(id)
            );
            """)

    def execute_query(self, query, params=None):
        with self.connection:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        self.connection.close()
