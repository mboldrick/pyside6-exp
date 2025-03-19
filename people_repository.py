class PeopleRepository:
    def __init__(self, db):
        """
        Initialize with an instance of the Database class.
        """
        self.db = db

    def list_people(self):
        query = "SELECT id, name FROM people"
        return self.db.execute_query(query)

    def create_person(self, name):
        with self.db.connection:
            cursor = self.db.connection.cursor()
            cursor.execute("INSERT INTO people (name) VALUES (?)", (name,))
            return cursor.lastrowid

    def update_person(self, person_id, name):
        with self.db.connection:
            cursor = self.db.connection.cursor()
            cursor.execute("UPDATE people SET name = ? WHERE id = ?", (name, person_id))
            return cursor.rowcount

    def delete_person(self, person_id):
        with self.db.connection:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM people WHERE id = ?", (person_id,))
            return cursor.rowcount
