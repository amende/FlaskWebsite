from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from dotenv import load_dotenv
import os

# local files:
from models import User, Timbre, db


# Load environment variables
load_dotenv()


# App initialisation
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Database initialisation
db.init_app(app)

# Just for easier debug
if os.getenv("debug"):
    with app.app_context():
        # db.drop_all()
        db.create_all()


# Login manager initialisation
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/signup')
def signup():
    return(render_template('signup.html'))


@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        return(redirect(url_for('signup')))

    new_user = User(email=email, name=name, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Bad email/password combination')
        return(render_template('login.html'))

    if user.password == password:
        login_user(user)
        return(redirect(url_for('profile')))
    else:
        flash('Bad email/password combination')
        return(render_template('login.html'))


# gestion de la collection:


@app.route('/maCollec')
@login_required
def maCollec():
    user = current_user
    timbres = Timbre.query.filter_by(owner=user.id)
    return(render_template("maCollec.html", timbres=timbres))


@app.route('/ajoutTimbre', methods=['GET', 'POST'])
@login_required
def ajoutTimbre():
    if request.method == 'GET':
        return(render_template("addTimbre.html"))
    if request.method == 'POST':
        nom = request.form.get('name')
        annee = request.form.get('date')
        owner = current_user.id
        new_timbre = Timbre(nom=nom, annee=annee, owner=owner)
        db.session.add(new_timbre)
        db.session.commit()
        return(redirect(url_for("maCollec")))


# Recherche de timbres
@app.route('/searchStamp', methods=['GET', 'POST'])
@login_required
def searchStamp():
    if request.method == 'GET':
        timbres = Timbre.query.all()
        return(render_template("search.html", timbres=timbres))
    if request.method == 'POST':
        min_year = request.form.get('min_year')
        if min_year is None:
            min_year = 0

        max_year = request.form.get('max_year')
        if max_year is None:
            max_year = 3000

        name = request.form.get('name')
        if name is None:
            name = ""

        timbres = Timbre.query.filter_by(Timbre.annee > min_year, Timbre.annee < max_year, name in Timbre.nom).all()
        return(render_template("search.html", timbres=timbres))


# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("debug"))
