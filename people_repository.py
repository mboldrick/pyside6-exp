class PeopleRepository:
    def __init__(self, db):
        """Initialize with an instance of the Database class."""
        self.db = db

    def list_people(self):
        query = "SELECT * FROM people"
        return self.db.execute_query(query)

    def create_person(self, name, email=None, phone=None, person_type='individual',
                    company_name=None, status='active', notes=None):
        """
        Insert a new person into the people table and return the new record's ID.

        :param name: The person's name (required).
        :param email: Optional email address.
        :param phone: Optional phone number.
        :param person_type: Either 'individual' or 'company' (default is 'individual').
        :param company_name: Optional company name if person_type is 'company'.
        :param status: Either 'active' or 'inactive' (default is 'active').
        :param notes: Optional notes.
        :return: The ID of the newly created person.
        """
        with self.db.connection:
            cursor = self.db.connection.cursor()
            cursor.execute("""
            INSERT INTO people (name, email, phone, type, company_name, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, person_type, company_name, status, notes))
            return cursor.lastrowid

    def get_person(self, person_id):
        query = "SELECT * FROM people WHERE id = ?"
        result = self.db.execute_query(query, (person_id,))
        return result[0] if result else None

    def update_person(self, person_id, name, email, phone, person_type, company_name, status, notes):
        with self.db.connection:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                UPDATE people
                SET name = ?, email = ?, phone = ?, type = ?, company_name = ?, status = ?, notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (name, email, phone, person_type, company_name, status, notes, person_id))
            return cursor.rowcount

    def delete_person(self, person_id):
        with self.db.connection:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM people WHERE id = ?", (person_id,))
            return cursor.rowcount
