from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
import hashlib
import logging
import os

if os.path.exists('logs/report.log'):
    with open('logs/report.log', 'w') as file:
        file.close()
    
logging.basicConfig(
    filename=""
)

app = Flask(__name__)
password_hash = hashlib.sha256()


db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
cursor = db.cursor(dictionary=True)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method  == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_hash.update(password.encode())
        hash_password = password_hash.hexdigest()
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        value = (email, hash_password)
        try:
            cursor.execute(query, value)
            db.commit()
            print("the register was succesfull")
            redirect(url_for('home'))
        except:
            print("something went wrong when updating the database")

    render_template('login.html')

@app.route('/logout')
def logout():
    pass

@app.route('/user')
def user():
    pass

@app.route('/user/favorite')
def favorite():
    pass

@app.route('/user/history')
def borrow_history():
    pass

@app.route('/books')
def books():
    pass

@app.route('/books/<int:book_id>')
def book_details(book_id):
    pass

@app.route('/books/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
   pass

@app.route('/books/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    pass

@app.route('/search')
def search():
    pass

@app.route('/admin')
def admin_dashboard():
    pass

@app.route('/admin/books/add', methods=['GET', 'POST'])
def add_book():
    pass

@app.route('/admin/books/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    pass

@app.route('/admin/books/remove/<int:book_id>', methods=['GET', 'POST'])
def remove_book():
    pass

@app.route('/about_us')
def about_us():
    pass

@app.route('/faq')
def faq():
    pass

if __name__ == "__main__":
    app.run(debug=True)