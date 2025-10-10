from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

# Routes

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# Run

if __name__ == "__main__":
    app.run(debug=True)