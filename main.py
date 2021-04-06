import flask
from flask_login import LoginManager, login_required
# from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from models import User, db

# App initialisation
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database initialisation
db.init_app(db)

# Just for easier debug
if os.getenv("debug"):
    db.drop_all()
    db.create_all()

# Login manager initialisation
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Load environment variables
load_dotenv()

@app.route('/')
def home():
    return flask.render_template('home.html')

@login_required
@app.route('/profile')
def profile():
    return flask.render_template('notYet.html')

@app.route('/signup')
def signup():
    return flask.render_template('notYet.html')

@app.route('/logout')
def logout():
    return flask.render_template('notYet.html')

@app.route('/login')
def login():
    return flask.render_template('login.html')


# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("debug"))
