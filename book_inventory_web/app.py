from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.exceptions import abort

# --- FLASK INITIALIZATION (CRITICAL) ---
app = Flask(__name__) 
DATABASE = 'inventory.db'

os.environ['FLASK_APP'] = 'app.py' 
os.environ['FLASK_ENV'] = 'development'
# ---------------------------------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE) 
    conn.row_factory = sqlite3.Row
    return conn

def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM Books WHERE book_id = ?', (book_id,)).fetchone()
    
    if book is None:
        abort(404) 
    
    author = conn.execute('SELECT first_name, last_name FROM Authors WHERE author_id = ?', (book['author_id'],)).fetchone()
    conn.close()
    
    return book, author

# 1. READ Route
@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute("SELECT B.book_id, B.title, B.publication_year, B.quantity_in_stock, B.isbn, A.first_name, A.last_name FROM Books B INNER JOIN Authors A ON B.author_id = A.author_id ORDER BY B.title").fetchall()
    conn.close()
    return render_template('index.html', books=books)

# 2. CREATE Route
@app.route('/add', methods=('GET', 'POST'))
def add_book():
    conn = get_db_connection()
    authors = conn.execute("SELECT author_id, first_name, last_name FROM Authors ORDER BY last_name").fetchall()
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        isbn = request.form['isbn']
        year = request.form['publication_year']
        stock = request.form['quantity_in_stock']
        conn.execute("INSERT INTO Books (title, author_id, isbn, publication_year, quantity_in_stock) VALUES (?, ?, ?, ?, ?)", (title, author_id, isbn, year, stock))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('add_book.html', authors=authors) 

# 3. UPDATE Route (Handles both GET (form display) and POST (data submission))
@app.route('/edit/<int:book_id>', methods=('GET', 'POST'))
def edit_book(book_id):
    book, author = get_book(book_id)
    
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        year = request.form['publication_year']
        stock = request.form['quantity_in_stock']
        
        conn = get_db_connection()
        conn.execute("UPDATE Books SET title = ?, isbn = ?, publication_year = ?, quantity_in_stock = ? WHERE book_id = ?", (title, isbn, year, stock, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index')) 

    # Renders the missing template!
    return render_template('edit_book.html', book=book, author=author)

# 4. DELETE Route
@app.route('/delete/<int:book_id>', methods=('POST',))
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM Books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 5. AGGREGATION Route
@app.route('/summary')
def stock_summary():
    conn = get_db_connection()
    summary = conn.execute("SELECT A.first_name, A.last_name, SUM(B.quantity_in_stock) AS total_stock, COUNT(B.book_id) AS total_books_count FROM Authors A LEFT JOIN Books B ON A.author_id = B.author_id GROUP BY A.author_id, A.first_name, A.last_name ORDER BY total_stock DESC").fetchall()
    conn.close()
    return render_template('summary.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
