from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user
from dotenv import load_dotenv
import os

# Initialization

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

secret = os.getenv("secret_key")

app.config['SECRET_KEY'] = secret

db = SQLAlchemy(app)

Migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

class Albums(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    year = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable = False)
    cover = db.Column(db.String(200), nullable = False)


# Routes

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        signuser = request.form.get('signuser')
        signpass = request.form.get('signpass')
        signpassconfirm = request.form.get('signpassconfirm')

        loguser = request.form.get('loguser')
        logpass = request.form.get('logpass')


        if signuser and signpass:
            if signpass == signpassconfirm:
                hashed_pw = bcrypt.generate_password_hash(signpass).decode('utf-8')
                new_user = Users(username=signuser, password=hashed_pw)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    flash("Signup Successful", "success")
                    return redirect(url_for('home'))
                except Exception as e:
                    db.session.rollback()
                    flash("Username Already Taken", 'fail')
                    return redirect(url_for('login'))
            else:
                flash("Passwords Do Not Match", "fail")
                return redirect(url_for('login'))
                

        if loguser and logpass:
           user = Users.query.filter_by(username=loguser).first()
           if user and bcrypt.check_password_hash(user.password, logpass):
               login_user(user)
               flash("Login Successful", 'success')
               return redirect(url_for('home'))
           else:
               flash("Incorrect Credintials", 'fail')
               return redirect(url_for('login'))    


@app.route("/explore")
@login_required
def explore():
    return render_template('explore.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully Logged Out", 'success')
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template("profile.html")
    if request.method == 'POST':
        pass

@app.route("/about/<album_id>", methods=['GET', 'POST'])
def about(album_id):
    album = albums.get(album_id)
    if not album:
        flash("Invalid Album", 'fail')
        return redirect(url_for("explore"))
    if request.method == 'GET':
        return render_template("about.html")
    if request.method == 'POST':
        pass
    
# Run

if __name__ == "__main__":
    app.run(debug=True)