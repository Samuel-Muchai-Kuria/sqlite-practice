import sqlite3

# Initialize DB
conn = sqlite3.connect("database/contacts.db")
# Create cursor for executing SQL commands
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE NOT NULL
)
""")
conn.commit()

def add_contact(name, phone, email, cursor=cursor, conn=conn):
    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    return "Contact added."

def view_contacts(cursor=cursor):
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    if not rows:
        return "No contacts found.\n"
    result = ""
    for row in rows:
        result += f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}\n"
    print(result)
    return result

def delete_contact(contact_id, cursor=cursor, conn=conn):
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    return "Contact deleted."

def search_name(name, cursor=cursor):
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + name + '%',))
    rows = cursor.fetchall()
    if not rows:
        return "No contacts found.\n"
    result = ""
    for row in rows:
        result += f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}\n"
    return result


def main():
    name= 'Alice Smith'
    phone = '123-456-7890'
    email = 'alice@example.com'
    add_contact(name, phone, email,
                 cursor=cursor, conn=conn)
    view_contacts(cursor=cursor)
    search_name("Alice", cursor=cursor)
    #delete the whole contact book
    cursor.execute("DELETE FROM contacts")
    conn.commit()

if __name__ == "__main__":
    main()
    conn.close()  # Close the connection when done