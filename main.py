import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# App and Database initialisation
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Just for easier debug
if os.getenv("debug"):
    db.drop_all()
    db.create_all()


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/login')
def login():
    return flask.render_template('login.html')


if __name__ == '__main__':
    app.run(debug=os.getenv("debug"))
