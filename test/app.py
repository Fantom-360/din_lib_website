#naimportíš kokotiny
from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
from PIL import Image
import os

#stateneš nejduležitější
app = Flask(__name__)
try:
    db = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    cursor=db.cursor()
except:
    #stránky
    @app.route('/')
    def home():
        return render_template('home.html')


    app.config["UPLOAD_FOLDER"] = "test/static/images"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    @app.route('/pictures', methods=['GET', 'POST'])
    def pictures():
        if request.method == 'POST':
            file = request.files.get('file')
            if file and file.filename.endswith(".png"):
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file = Image.open(file)
                gray_file = file.convert('L')
                gray_file.save(file_path)
                return redirect(url_for('home'))
        
        return render_template('pictures.html')
    
    @app.route("/user/<int:user_id>")
    def show_user(user_id):
        message = None
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        if user:
            username, password, email = user
            print(f"\nUser: {user_id}, \nPassword:{password}, \nUsername: {username}, \nEmail: {email}\n")
            
            return redirect(url_for('home'))
        else:
            message = "This user doesnt exist"
            return render_template('user.html', message = message)
            
    @app.route('/print_text', methods=['GET','POST'])
    def print_text():
        if request.method == 'POST':
            text = request.form.get('text')
            num = int(request.form.get('num'))

            for _ in range(num):
                print(text)

            return redirect(url_for('home'))

        return render_template('text_mult.html')
    
    @app.route('/sitepics')
    def podm():
        x = 0
        left_png, right_png, text = None, None, None

        if x == 0: 
            left_png, right_png = True, True
        elif x == 1: 
            left_png = True
        elif x == 2: 
            right_png = True
        else: 
            text = "Bohužel při sartu nastala chyba! Zkuste přepsat neznámou a restartovat server!"

        return render_template('random.html', left_png = left_png, right_png = right_png, text = text)

    if __name__ == "__main__":
        app.run(debug=True)