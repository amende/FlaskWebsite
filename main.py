from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import random
import string
import os
import datetime

# local files:
from models import User, Timbre, db, Message


# Load environment variables
load_dotenv()


# App initialisation
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# gestion des upload images des timbres
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

    user = User.query.filter_by(name=name).first()
    if user:
        flash("This username is already taken.")
        return(redirect(url_for('signup')))

    user = User.query.filter_by(email=email).first()
    if user:
        flash("An account already exists for this email.")
        return(redirect(url_for('signup')))

    new_user = User(email=email, name=name, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash("Account has been created, now please login.")
    return redirect(url_for("login"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully logged out")
    return render_template('home.html')


@app.route('/editProfile', methods=['POST'])
@login_required
def editProfile():
    notif_success = False

    name = request.form.get('name')
    if name != "":
        current_user.name = name
        notif_success = True

    email = request.form.get('email')
    if email != "":
        current_user.email = email
        notif_success = True

    password = request.form.get('password')
    if password != "":
        current_user.password = password
        notif_success = True

    if notif_success:
        flash("Successfully edited profile")

    db.session.commit()
    return render_template('profile.html')


@app.route('/deleteProfile')
@login_required
def deleteProfile():
    User.query.get(current_user.id).delete()
    db.session.commit()
    logout_user()
    flash("Successfully deleted profile")
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
        # gestion de l'image
        if 'file' not in request.files:
            securedFileName = 'images/img_wireframe.png'
        else:
            file = request.files['file']
            if file.filename == '':
                securedFileName = 'images/img_wireframe.png'
            if file and allowed_file(file.filename):
                letters = string.ascii_lowercase
                randomName = ''.join(random.choice(letters) for i in range(15))
                securedFileName = 'images/upload/'+randomName
                cheminSauvegarde = os.path.join(app.config['UPLOAD_FOLDER'], randomName)
                file.save(cheminSauvegarde)
        # en bdd
        name = request.form.get('name')
        year = request.form.get('date')
        owner = current_user.id
        isPublic = request.form.get('isPublic') == 'on'
        new_timbre = Timbre(name=name, year=year, owner=owner, isPublic=isPublic, fileName=securedFileName)
        db.session.add(new_timbre)
        db.session.commit()
        return(redirect(url_for("maCollec")))


# Recherche de timbres
@app.route('/searchStamp', methods=['GET', 'POST'])
@login_required
def searchStamp():
    if request.method == 'GET':
        timbres = Timbre.query.filter_by(isPublic=True).limit(50)
        return(render_template("search.html", timbres=timbres))
    if request.method == 'POST':
        min_year = request.form.get('min_year')
        if min_year == "":
            min_year = 0

        max_year = request.form.get('max_year')
        if max_year == "":
            max_year = 3000

        name = request.form.get('name')

        timbres = Timbre.query.filter(Timbre.name.ilike('%'+name+'%'))   \
                              .filter(Timbre.year >= min_year, Timbre.year <= max_year)   \
                              .filter_by(isPublic=True).limit(50)
        return(render_template("search.html", timbres=timbres))


# Message
@app.route('/messaging', methods=['GET', 'POST'])
@login_required
def messaging():

    if request.method == 'POST':
        timestamp = datetime.datetime.now()
        sender = current_user.id
        receiver = User.query.filter_by(name=request.form.get('receiver')).first().id
        content = request.form.get('content')
        seen = False
        new_message = Message(timestamp=timestamp, sender=sender, receiver=receiver, content=content, seen=seen)
        db.session.add(new_message)
        db.session.commit()

    # Getting received messages
    messagesReceivedQuery = Message.query.filter_by(receiver=current_user.id)
    messagesReceived = []

    for message in messagesReceivedQuery:
        date = f"{message.timestamp:%Y/%m/%d %H:%M}"
        sender = User.query.filter_by(id=message.sender).first().name
        content = message.content
        if not message.seen :
            message.seen = True
            db.session.commit()
        seen = message.seen
        messagesReceived.append({"date": date, "sender": sender, "content": content, "seen": seen})

    # Getting sent messages
    messagesSentQuery = Message.query.filter_by(sender=current_user.id)
    messagesSent = []

    for message in messagesSentQuery:
        date = f"{message.timestamp:%Y/%m/%d %H:%M}"
        receiver = User.query.filter_by(id=message.receiver).first().name
        content = message.content
        seen = message.seen
        messagesSent.append({"date": date, "receiver": receiver, "content": content, "seen": seen})

    return(render_template("messaging.html", messagesReceived=messagesReceived, messagesSent=messagesSent))


# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("debug"))
