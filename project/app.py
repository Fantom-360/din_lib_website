from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
import hashlib
import mysql.connector

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    database = "library"
)
cursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = "something_meow"

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confr_password = request.form.get("confirm_password")

        if password != confr_password:
            flash("Passwords do not match!", "error")
            return redirect("/register")
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        query = "INSERT INTO register (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password_hash)

        
        cursor.execute(query, values)
        mydb.commit()
        flash("you have sucessfuly registred", "success")
        return redirect("/login")
        
    return render_template("register.html")

@app.route('/borrow_book/<book_id>')
def borrow_book(book_id):
    if "user_id" not in session:
        flash("you need to be log in to borrow books!", "error")
        return redirect(url_for("home"))
    
    user_id = session["user_id"]
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book or book["available"] == 0:
        flash("Book is already borrowed!", "error")
        return redirect(url_for("home"))
    borrow_date = datetime.today().date()
    return_date = borrow_date + timedelta(days=28)
    cursor.execute(
        "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)",
        (user_id, book_id, borrow_date, return_date)
    )
    cursor.execute("UPDATE books SET available = 0 WHERE id = %s", (book_id,))
    mydb.commit()
    cursor.close()
    flash("Book borrowed successfully!", "success")
    return redirect(url_for("home"))

@app.route('/return_book/<int:book_id>')
def return_book(book_id):

    if "user_id" not in session:
        flash("You need to be logged in", "error")
        return redirect(url_for("login"))
    user_id = session["user_id"]
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT * FROM borrowd_books WHERE book_id = %s AND user_id = %s", (book_id, user_id)
    )
    borrowed = cursor.fetchone()

    if not borrowed:
        flash("You haven't borrowed this book!", "error")
        return redirect(url_for("home"))
    cursor.execute("DELETE FROM borrowed_books WHERE book_id = %s AND user_id = %S", (book_id, user_id))
    mydb.commit()
    cursor.close()
    flash("Book returned successfully!", "success")
    return redirect(url_for("home"))

@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor = mydb.cursor(dictionary=True)
        query = "SELECT * FROM register WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user["password"] == hashlib.sha256(password.encode()).hexdigest():
            session["user_id"] = user["id"] if "id" in user else None
            session["username"] = user["username"]
            flash("login succesful!", "success")
            return redirect(url_for("home"))
        
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("index0.html")

@app.route("/books")
def books():
    genre = request.args.get('genre')
    cursor = mydb.cursor(dictionary=True)
    if genre:
        cursor.execute("SELECT * FROM books WHERE genre = %s", (genre,))
    else:
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()
    cursor.close()
    return jsonify(books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %d")
    book = cursor.fetchone()
    cursor.close()
    return jsonify(book)

@app.route("/sign_up")
def sing():
    return render_template("index2.html")

@app.route("/log_in")
def login():
    return render_template("index3.html")

@app.route('/admin', methods=['POST', 'GET'])
def admlog():

    if request.method == 'POST':
        password = request.form.get('password')
        cursor = mydb.cursor(dictionary=True)
        query = "SELECT password FROM register WHERE id = %s"
        cursor.execute(query, (1,))
        passwordadm = cursor.fetchone()
        cursor.close()

        if password == passwordadm[0]:
            session['user'] = 'admin'
            flash("Admin logged in succesfullly", "success")
            return redirect('/admin/add_book')
        
        else:
            flash("try another password", "error")

            return redirect('/admin')
        
    return render_template("adminlog.html")

@app.route('/admin/add_book', methods=['POST'])
def add_book():
    
    if 'admin' not in session:
        return jsonify({"error": "Admin login required"})

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect('/login')
    
if __name__ == "__main__":
    app.run(debug=True)