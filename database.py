import sqlite3
from pathlib import Path


db_path = Path("invoice3001.db")
if not db_path.exists():
  print("Database file does not exist. It will be created now.")

class Database:
    def __init__(self, db_name="invoice3001.db"):
        """Initialize the database connection."""
        self.db_name = db_name
        self._ensure_tables_exist()

    def _connect(self):
        """Establish a connection to the database."""
        return sqlite3.connect(self.db_name)

    def _ensure_tables_exist(self):
        """Ensures tables exist before inserting data."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='people';")
        if cursor.fetchone() is None:
            print("The 'people' table does not exist. Creating the table now.")
            cursor.execute("""
                CREATE TABLE people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT CHECK (type IN ('individual', 'company')),
                company_name TEXT,
                email TEXT,
                phone TEXT
                );
            """)
            conn.commit()
        else:
            print("The 'people' table already exists.")


        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT CHECK (type IN ('individual', 'company')),
            company_name TEXT,
            email TEXT,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            legacy_id TEXT,
            name TEXT NOT NULL,
            start_date TEXT,
            client_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES people(id) ON DELETE CASCADE
        );
        """)
        conn.commit()
        conn.close()

    def load_clients(self):
        """Fetches all clients from the database."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, type, email, phone FROM people")
        clients = cursor.fetchall()
        conn.close()
        return clients

    def client_exists(self, name):
        """Checks if a client already exists by name."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM people WHERE name = ?", (name,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def get_client_by_id(self, client_id):
        """Fetches client details before deletion (for Undo)."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM people WHERE id = ?", (client_id,))
        client = cursor.fetchone()
        conn.close()
        return client

    def get_client_name(self, client_id):
        """Returns the name of a client by ID."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM people WHERE id = ?", (client_id,))
        name = cursor.fetchone()
        conn.close()
        return name[0] if name else None

    def add_client(self, name, email, client_type="individual"):
        """Inserts a new client into the database."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO people (name, type, email) VALUES (?, ?, ?)",
            (name, client_type, email),
        )
        conn.commit()
        conn.close()

    def delete_client(self, client_id):
        """Deletes a client and their associated projects."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM people WHERE id = ?", (client_id,))
        conn.commit()
        conn.close()

    def update_client(self, client_id, name, email):
        """Updates an existing client's information."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE people SET name = ?, email = ? WHERE id = ?",
            (name, email, client_id),
        )
        conn.commit()
        conn.close()

    def restore_client(self, client):
        """Restores a deleted client using cached data."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO people (id, name, email) VALUES (?, ?, ?)",
            (client[0], client[1], client[2]),
        )
        conn.commit()
        conn.close()

    def client_has_projects(self, client_id):
        """Checks if a client has projects."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM projects WHERE client_id = ?", (client_id,)
        )
        has_projects = cursor.fetchone()[0] > 0
        conn.close()
        return has_projects

    def load_projects(self, client_id):
        """Fetches projects associated with a specific client."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, legacy_id, name, start_date FROM projects WHERE client_id = ?",
            (client_id,),
        )
        projects = cursor.fetchall()
        conn.close()
        return projects
