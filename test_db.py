import unittest
import sqlite3
from contact_book import add_contact, view_contacts, delete_contact, conn, cursor

class TestContactBook(unittest.TestCase):

    def setUp(self):
        # Use in-memory DB for tests (optional: use ':memory:')
        self.test_conn = sqlite3.connect(':memory:')  # in-memory temporary DB
        self.test_cursor = self.test_conn.cursor()

        # Create table
        self.test_cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
        """)
        
        self.test_conn.commit()

    def test_add_contact(self):
        result = add_contact("John Doe", "123456789", "john@example.com",
                             cursor=self.test_cursor, conn=self.test_conn)
        self.assertEqual(result, "Contact added.")

        self.test_cursor.execute("SELECT * FROM contacts WHERE name = 'John Doe'")
        rows = self.test_cursor.fetchall()
        self.assertEqual(len(rows), 1)
        self.test_cursor.execute("DELETE FROM contacts")
        self.test_conn.commit()

    def test_view_contacts(self):
        add_contact("Jane Doe", "987654321", "jane@example.com",
                     cursor=self.test_cursor, conn=self.test_conn)
        output = view_contacts(self.test_cursor)
        self.assertIn("Jane Doe", output)

    def test_delete_contact(self):
        add_contact("Temp User", "000", "temp@example.com",
                     cursor=self.test_cursor, conn=self.test_conn)
        self.test_cursor.execute("SELECT id FROM contacts WHERE name = 'Temp User'")
        contact_id = self.test_cursor.fetchone()[0]

        result = delete_contact(contact_id, cursor=self.test_cursor, conn=self.test_conn)
        self.assertEqual(result, "Contact deleted.")

        self.test_cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        self.assertEqual(self.test_cursor.fetchall(), [])

    def tearDown(self):
        self.test_conn.close()

if __name__ == '__main__':
    unittest.main()
