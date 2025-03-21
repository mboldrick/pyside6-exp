
import sqlite3

class Database:
    def __init__(self, db_name="billing.db"):
        """Initialize the database connection."""
        self.db_name = db_name
        self.connection = self._connect_sqlite()
        self._ensure_tables_exist()

    def _connect_sqlite(self):
        """Establish a connection to the database."""
        return sqlite3.connect(self.db_name)

    def _ensure_tables_exist(self):
        """Ensures tables exist before inserting data."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                type TEXT CHECK (type IN ('individual', 'company')),
                company_name TEXT,
                status TEXT CHECK (status IN ('active', 'inactive')),
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TRIGGER IF NOT EXISTS update_person_updated_at
                AFTER UPDATE ON people
                FOR EACH ROW
                BEGIN
                    UPDATE people
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE id = OLD.id;
                END;

            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                address_line1 TEXT,
                address_line2 TEXT,
                city TEXT,
                state TEXT,
                country TEXT NOT NULL DEFAULT 'USA',
                postal_code TEXT,
                type TEXT CHECK(type IN ('home', 'work', 'other')),
                preferred INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES people(id)
            );

            CREATE TRIGGER IF NOT EXISTS update_address_updated_at
                AFTER UPDATE ON addresses
                FOR EACH ROW
                BEGIN
                    UPDATE addresses
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE id = OLD.id;
                END;

            CREATE TABLE IF NOT EXISTS chart_of_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                acct_code TEXT,
                acct_name TEXT NOT NULL,
                acct_type TEXT CHECK (acct_type IN ('Asset', 'Liability', 'Equity', 'Revenue', 'COGS', 'Expense', 'Other Expense')),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount INTEGER NOT NULL,
                category_id INTEGER,
                description TEXT,
                date TEXT,
                person_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES chart_of_accounts(id),
                FOREIGN KEY (person_id) REFERENCES people(id)
            );

            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS work_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                project_id INTEGER,
                hours REAL,
                date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
