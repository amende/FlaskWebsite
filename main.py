import flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for, request
from dotenv import load_dotenv
import os




# App and Database initialisation
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
# Just for easier debug
if os.getenv("debug"):
    db.drop_all()
    db.create_all()

# Load environment variables
load_dotenv()




@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/profile')
def profile():
    return flask.render_template('notYet.html')

@app.route('/signup')
def signup():
    return(render_template('signup.html'))

@app.route('/signup',methods=['POST'])
def signup_post():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')

    user=User.query.filter_by(email=email).first()
    if user:
        return(redirect(url_for('signup')))

    new_user=User(email=email,name=name,password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    return flask.render_template('notYet.html')


@app.route('/login')
def login():
    return flask.render_template('login.html')
    




# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("debug"))
