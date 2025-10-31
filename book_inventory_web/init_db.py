import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Books;")
cursor.execute("DROP TABLE IF EXISTS Authors;")

cursor.execute("""
CREATE TABLE Authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50)
);
""")

cursor.execute("""
CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_year INTEGER,
    quantity_in_stock INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
);
""")

cursor.execute("INSERT INTO Authors (first_name, last_name, nationality) VALUES ('Gabriel', 'Garcia Marquez', 'Colombian')")
gabo_id = cursor.lastrowid

cursor.execute("INSERT INTO Authors (first_name, last_name, nationality) VALUES ('Harper', 'Lee', 'American')")
harper_id = cursor.lastrowid

cursor.execute("INSERT INTO Authors (first_name, last_name, nationality) VALUES ('George', 'Orwell', 'British')")
george_id = cursor.lastrowid

cursor.execute("INSERT INTO Authors (first_name, last_name, nationality) VALUES ('Toni', 'Morrison', 'American')")
toni_id = cursor.lastrowid

cursor.execute("INSERT INTO Books (title, author_id, isbn, publication_year, quantity_in_stock) VALUES (?, ?, '978-0060953101', 1967, 12)", ('One Hundred Years of Solitude', gabo_id))
cursor.execute("INSERT INTO Books (title, author_id, isbn, publication_year, quantity_in_stock) VALUES (?, ?, '978-0061120084', 1960, 25)", ('To Kill a Mockingbird', harper_id))
cursor.execute("INSERT INTO Books (title, author_id, isbn, publication_year, quantity_in_stock) VALUES (?, ?, '978-0451524935', 1949, 18)", ('1984', george_id))
cursor.execute("INSERT INTO Books (title, author_id, isbn, publication_year, quantity_in_stock) VALUES (?, ?, '978-1400033416', 1987, 6)", ('Beloved', toni_id))

conn.commit()
conn.close()

print("Database 'inventory.db' created and populated successfully.")