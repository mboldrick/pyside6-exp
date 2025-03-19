import sqlite3

try:
  import psycopg2
except ImportError:
  psycopg2 = None

class Database:
  def __init__(self, backend="sqlite", db_name="billing.db", **kwargs):
    """
    Initialize the database connection.

    For SQLite:
      - backend="sqlite", db_name is the file name.

    For PostgreSQL:
      - backend="postgresql", pass additional connection parameters as kwargs.
    """
    self.backend = backend.lower()
    self.connection_params = kwargs
    if self.backend == "sqlite":
      self.db_name = db_name
      self.connection = self._connect_sqlite()
    elif self.backend == "postgresql":
      self.connection = self._connect_postgresql()
    else:
      raise ValueError(f"Unsupported backend: {backend}")

    self._ensure_tables_exist()

  def _connect_sqlite(self):
    return sqlite3.connect(self.db_name)

  def _connect_postgresql(self):
    if psycopg2 is None:
      raise ImportError("psycopg2 is required for PostgreSQL connections")
    return psycopg2.connect(**self.connection_params)

  def _ensure_tables_exist(self):
    if self.backend == "sqlite":
      self._ensure_tables_exist_sqlite()
    elif self.backend == "postgresql":
      self._ensure_tables_exist_postgresql()

  def _ensure_tables_exist_sqlite(self):
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

  def _ensure_tables_exist_postgresql(self):
    with self.connection:
      cursor = self.connection.cursor()
      # PostgreSQL uses slightly different SQL syntax.
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255) NOT NULL
        );
      """)
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS expense_categories (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255) NOT NULL
        );
      """)
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
          id SERIAL PRIMARY KEY,
          amount NUMERIC NOT NULL,
          category_id INTEGER REFERENCES expense_categories(id),
          description TEXT,
          date DATE
        );
      """)
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          start_date DATE,
          end_date DATE
        );
      """)
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_log (
          id SERIAL PRIMARY KEY,
          person_id INTEGER REFERENCES people(id),
          project_id INTEGER REFERENCES projects(id),
          hours NUMERIC,
          date DATE
        );
      """)
      # For psycopg2, you may need an explicit commit if not using a context manager.
      self.connection.commit()

  def execute_query(self, query, params=None):
    """
    Execute a query and return all fetched rows.
    """
    with self.connection:
      cursor = self.connection.cursor()
      if params:
        cursor.execute(query, params)
      else:
        cursor.execute(query)
      return cursor.fetchall()

  def close(self):
    self.connection.close()
